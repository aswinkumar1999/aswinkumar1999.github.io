"""Build the eval-gallery: tiny 4× clips + posters + data.json for every rollout.

Reads trials.json (one folder up from submission/), dedups resume runs, and for
each (dataset, episode) pair, writes:
  - clips/<dataset>__epNN.mp4   (128×72, 4× speed baked in)
  - posters/<dataset>__epNN.jpg (mid-clip frame)
  - data.json                   (one entry per tile, consumed by index.html)

Idempotent — skips clips that already exist.

Run:
  python build_gallery.py
"""
import json, re, subprocess, sys, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

GALLERY = Path(__file__).resolve().parent
SUBMISSION = GALLERY.parent
SESSION = SUBMISSION.parent
TRIALS = SESSION / "trials.json"
DATASETS = SESSION / "datasets"
PRESPLIT = SESSION / "vlm_pipeline" / "datasets_split"
CLIPS = GALLERY / "clips"
CLIPS_LO = GALLERY / "clips_lo"
POSTERS = GALLERY / "posters"
CLIPS.mkdir(exist_ok=True)
CLIPS_LO.mkdir(exist_ok=True)
POSTERS.mkdir(exist_ok=True)

RESUME_RE = re.compile(r"-\d{8}_\d{6}$")


def detect_cams(df):
    """Same logic as vlm_pipeline/01_prep_dataset.py::detect_cams."""
    cams = sorted({c.split("/")[1] for c in df.columns if c.startswith("videos/")})
    overhead = next(
        (c for k in ("overhead", "base_0_rgb", "base", "top") for c in cams if k in c.lower()),
        cams[0],
    )
    return overhead


def variant_from_dataset(name, policy):
    """`block-st2-pi05-task1task2-50-all` + Pi05 → `task1task2-50-all`"""
    # name is like block-st1-act-task1-all (no resume suffix at this point)
    parts = name.split("-")
    # parts: ['block','st1','act','task1','all']  → variant = parts[3:]
    # parts: ['block','st2','pi05','task1task2','50','all']
    # robust: drop block + st_x + policy_token, keep the rest
    return "-".join(parts[3:])


def base_name(ds_root_path):
    name = Path(ds_root_path).name
    return RESUME_RE.sub("", name)


def slice_episode_overhead(src_root, df, cam, ep_idx, dst):
    """Extract one episode's overhead clip via ffmpeg (from parquet timestamps)."""
    row = df[df.episode_index == ep_idx].iloc[0]
    f_idx = int(row[f"videos/{cam}/file_index"])
    c_idx = int(row[f"videos/{cam}/chunk_index"])
    t0 = float(row[f"videos/{cam}/from_timestamp"])
    t1 = float(row[f"videos/{cam}/to_timestamp"])
    src = src_root / "videos" / cam / f"chunk-{c_idx:03d}" / f"file-{f_idx:03d}.mp4"
    if not src.exists():
        raise FileNotFoundError(src)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{t0:.3f}", "-i", str(src), "-t", f"{t1-t0:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-an", str(dst),
    ], check=True)


def ffprobe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    try: return float(out.stdout.strip())
    except ValueError: return 0.0


def fallback_slice_no_parquet(src_root, ep_idx, dst, scratch_dir):
    """Used when meta/data parquets are corrupt.

    Reads info.json for total_episodes, finds an overhead-style camera folder,
    sums durations across chunk-000/file-NNN.mp4, divides total time equally,
    slices the chunk that contains ep_idx's time window.
    """
    info_p = src_root / "meta" / "info.json"
    info = json.load(open(info_p))
    n_eps = int(info.get("total_episodes", 0))
    if n_eps <= 0: raise RuntimeError("no total_episodes in info.json")
    if ep_idx >= n_eps: raise RuntimeError(f"ep_idx {ep_idx} >= total_episodes {n_eps}")

    # Find an overhead-style camera folder
    vids = src_root / "videos"
    cam_dir = next(
        (vids / d.name for d in vids.iterdir() if d.is_dir() and any(
            k in d.name.lower() for k in ("overhead", "base_0_rgb", "base", "camera1", "camera_1", "camera0", "camera_0", "top"))),
        None,
    )
    if cam_dir is None: raise RuntimeError("no overhead-like camera folder")

    chunk_dirs = sorted(cam_dir.glob("chunk-*"))
    files = []
    for cd in chunk_dirs:
        for mp4 in sorted(cd.glob("file-*.mp4")):
            files.append((mp4, ffprobe_duration(mp4)))
    total = sum(d for _, d in files)
    if total <= 0: raise RuntimeError("no playable mp4s in camera folder")

    # ep i spans [i*per_ep, (i+1)*per_ep)
    per_ep = total / n_eps
    t_start = ep_idx * per_ep
    t_end = (ep_idx + 1) * per_ep

    # Find which file contains t_start; slice from local offset
    cum = 0.0
    for path, dur in files:
        if t_start < cum + dur:
            local_start = max(0.0, t_start - cum)
            local_dur = min(dur - local_start, per_ep)
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error",
                "-ss", f"{local_start:.3f}", "-i", str(path),
                "-t", f"{local_dur:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-an", str(dst),
            ], check=True)
            return
        cum += dur
    raise RuntimeError(f"could not place ep {ep_idx} in concatenated timeline")


def find_or_make_source_clip(dataset_full_name, ep_idx, scratch_dir):
    """Return a path to a full-res overhead clip for (dataset, ep_idx).

    Try (in order):
      1. vlm_pipeline/datasets_split/<dataset>/<overhead_cam>/episode_NN_*.mp4
      2. Slice via parquet timestamps (datasets/<ds>/meta/episodes/*.parquet)
      3. Equal-time fallback when parquets are corrupt
    """
    presplit_root = PRESPLIT / dataset_full_name
    if presplit_root.exists():
        for cam_dir in presplit_root.iterdir():
            if not cam_dir.is_dir(): continue
            if not any(k in cam_dir.name.lower() for k in ("overhead", "base_0_rgb", "base")):
                continue
            hits = list(cam_dir.glob(f"episode_{ep_idx:02d}_*.mp4"))
            if hits:
                return hits[0]

    src_root = DATASETS / dataset_full_name
    if not src_root.exists():
        raise FileNotFoundError(src_root)

    scratch_dir.mkdir(parents=True, exist_ok=True)
    out = scratch_dir / f"{dataset_full_name}__ep{ep_idx:02d}.mp4"
    if out.exists(): return out

    parquets = list((src_root / "meta" / "episodes").rglob("*.parquet"))
    if parquets:
        try:
            df = pd.read_parquet(parquets[0])
            cam = detect_cams(df)
            slice_episode_overhead(src_root, df, cam, ep_idx, out)
            return out
        except Exception:
            pass  # fall through to fallback
    fallback_slice_no_parquet(src_root, ep_idx, out, scratch_dir)
    return out


def encode_tiny(src_path, tiny_path):
    # 480×270 @ crf 22 → sharp when scaled up to ~360×200 in the spotlight.
    # 4× speed baked in via setpts. ~700 KB per clip.
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src_path),
        "-vf", "setpts=PTS/4,scale=480:270,format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "22",
        "-movflags", "+faststart", "-g", "30",
        "-profile:v", "main", "-level", "4.0",
        str(tiny_path),
    ], check=True)


def encode_lo(src_path, lo_path):
    # 144×80, baseline profile, aggressive CRF — designed for ~80 simultaneous
    # decoders in the browser as ambient grayscale background.
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src_path),
        "-vf", "setpts=PTS/4,scale=144:80,format=yuv420p",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "32",
        "-movflags", "+faststart", "-g", "30",
        "-profile:v", "baseline", "-level", "3.0",
        str(lo_path),
    ], check=True)


def extract_poster(tiny_path, poster_path):
    # Get duration of the tiny clip; pick midpoint
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(tiny_path)],
        check=True, capture_output=True, text=True,
    )
    try:
        dur = float(out.stdout.strip())
    except ValueError:
        dur = 1.0
    mid = max(0.0, dur / 2)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", f"{mid:.3f}", "-i", str(tiny_path),
        "-frames:v", "1", "-q:v", "5", str(poster_path),
    ], check=True)


def process_one(args):
    """Worker: produce hi-res tiny clip + lo-res clip + poster for a single tile."""
    dataset_full, ep_idx, tile = args
    tile_id = f"{dataset_full}__ep{ep_idx:02d}"
    tiny = CLIPS / f"{tile_id}.mp4"
    lo = CLIPS_LO / f"{tile_id}.mp4"
    poster = POSTERS / f"{tile_id}.jpg"
    scratch = GALLERY / "_scratch_src"

    if tiny.exists() and lo.exists() and poster.exists():
        return tile_id, "skip"

    try:
        src = find_or_make_source_clip(dataset_full, ep_idx, scratch)
        if not tiny.exists():
            encode_tiny(src, tiny)
        if not lo.exists():
            encode_lo(src, lo)
        if not poster.exists():
            extract_poster(tiny, poster)
        return tile_id, "ok"
    except Exception as e:
        return tile_id, f"err: {type(e).__name__}: {str(e)[:80]}"


def main():
    print(f"Reading {TRIALS}")
    trials = json.load(open(TRIALS))
    print(f"  {len(trials)} trial entries")

    # Group by dataset_root → list of (started_at, trial)
    by_root = defaultdict(list)
    for t in trials:
        ds_root = t.get("dataset_root")
        if not ds_root: continue
        by_root[ds_root].append(t)

    # Sort each group by started_at. Do NOT dedup retry variants — they hold
    # disjoint trials (the retry folder records scenes the base didn't get to).
    # Each variant gets its own ep_idx 0..N-1 within its own recording session.
    print(f"  {len(by_root)} variant folders ({len(set(base_name(r) for r in by_root))} unique bases)")

    # Build the tile list
    tiles = []
    todo_jobs = []
    for ds_root, ts in sorted(by_root.items()):
        ts.sort(key=lambda t: t.get("started_at", ""))
        dataset_full = Path(ds_root).name
        for ep_idx, t in enumerate(ts):
            policy = t.get("architecture", "?")
            variant = variant_from_dataset(base_name(ds_root), policy)
            tile = {
                "id": f"{dataset_full}__ep{ep_idx:02d}",
                "clip": f"clips/{dataset_full}__ep{ep_idx:02d}.mp4",
                "clip_lo": f"clips_lo/{dataset_full}__ep{ep_idx:02d}.mp4",
                "poster": f"posters/{dataset_full}__ep{ep_idx:02d}.jpg",
                "subtask": t.get("eval_task", "?"),
                "policy": policy,
                "variant": variant,
                "scene": t.get("scene_id", ""),
                "success": bool(t.get("success", False)),
            }
            tiles.append(tile)
            todo_jobs.append((dataset_full, ep_idx, tile))

    print(f"  {len(tiles)} total tiles to build")

    # Build clips/posters in parallel
    t_start = time.time()
    ok = skipped = errs = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(process_one, j): j for j in todo_jobs}
        for f in as_completed(futs):
            tile_id, status = f.result()
            if status == "ok": ok += 1
            elif status == "skip": skipped += 1
            else:
                errs += 1
                print(f"  ✗ {tile_id}: {status}")
            done = ok + skipped + errs
            if done % 50 == 0 or done == len(futs):
                print(f"  [{done}/{len(futs)}] ok={ok} skip={skipped} err={errs} ({time.time()-t_start:.0f}s)")

    # Filter tiles to only ones whose artifacts exist
    final_tiles = [
        t for t in tiles
        if (CLIPS / f"{t['id']}.mp4").exists()
           and (CLIPS_LO / f"{t['id']}.mp4").exists()
           and (POSTERS / f"{t['id']}.jpg").exists()
    ]
    (GALLERY / "data.json").write_text(json.dumps(final_tiles, indent=2))
    print(f"\nWrote data.json with {len(final_tiles)} tiles "
          f"(dropped {len(tiles)-len(final_tiles)} that failed to build)")
    print(f"Wall: {time.time()-t_start:.0f}s")


if __name__ == "__main__":
    main()

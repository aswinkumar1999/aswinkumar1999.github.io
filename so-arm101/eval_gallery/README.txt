SO-ARM101 — Eval Gallery
========================

A Netflix-style ambient web page showing every robot rollout from the eval
sweep. Designed to leave open during Q&A after the presentation.

HOW TO VIEW
  1. Open a terminal in this folder.
  2. Run:  python3 -m http.server 8765
  3. Open http://localhost:8765/index.html in Chrome / Edge.

  (Direct file:// usually works too, but some browsers block autoplay there.)

WHAT YOU SEE
  • A grid of 465 tiny tiles, one per evaluation episode (overhead camera).
    (30 unique evals × 16 episodes = 480 expected; 15 trials never finished
    recording — info.json says total_episodes < trial count for those.)
  • Each tile shows a still frame from its episode in muted grayscale.
  • Every ~4 seconds, 3 random tiles light up in color, scale up like
    Netflix hero cards, and play their video at 4× speed.
  • Spotlights cycle through ACT (blue), SmolVLA (green), Pi05 (orange).
  • A spotlit tile shows 4 corner labels:
      top-left:    subtask (ST1 / ST2)
      top-right:   ✓ success / ✗ failure
      bottom-left: policy (ACT / SmolVLA / Pi05)
      bottom-right: dataset variant (e.g. task1-all, universal-all)

CONTENTS
  index.html        — the gallery page (self-contained, all CSS+JS inline)
  data.json         — one record per tile (metadata)
  clips/            — 128×72 mp4s, ~50 KB each, 4× speed baked in
  posters/          — middle-frame jpegs, ~3 KB each (shown when tile cold)
  build_gallery.py  — re-runnable build script

REBUILD AFTER NEW ROLLOUTS
  As new datasets land in ../../datasets/ and trials.json is updated by the
  eval harness, run:

      python3 build_gallery.py

  It's idempotent — existing tiles are skipped, new ones are encoded.

TUNING
  In index.html, top of the <script> block:
    HIGHLIGHT_COUNT       = 3      (tiles colored at any moment)
    HIGHLIGHT_INTERVAL_MS = 4000   (rotation period)

  In the CSS, .tile.hot { transform: scale(1.55); ... } controls how big
  spotlit tiles grow. Bump down to scale(1.3) for less drama.

BROWSER NOTES
  • Chrome/Edge tested.
  • Memory stays under ~250 MB (only 3 video decoders ever active).
  • Initial load fetches ~1.7 MB of posters; ~1-2 s splash on first open.

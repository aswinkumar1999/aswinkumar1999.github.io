---
layout: post
title: "Training a robot policy for a task with zero data — SO-ARM101 compositional study"
author: Aswinkumar
date: '2026-06-07 12:00:00 -0500'
category:
        - Robotics
        - Imitation Learning
        - CS839
        - UW-Madison
summary: "684 real-robot rollouts, 39 policies, 16 dataset recipes — and a held-out compositional task with no direct training data."
thumbnail: /so-arm101/plots/setup_marked.png
---

> **TL;DR** — For my CS839 final project at UW-Madison I designed a four-task pick-and-place ladder on the SO-ARM101 and asked: can the right *combination* of data on three known tasks teach a policy to do a fourth task it never saw a single demo for? Best policy got 9 out of 10 random scenes correct on the held-out task.
>
> **Full project page (with interactive eval gallery of all 661 rollouts):** [aswinkumar.me/so-arm101/](/so-arm101/)
> **Code:** [github.com/aswinkumar1999/so-arm101-imitation-learning](https://github.com/aswinkumar1999/so-arm101-imitation-learning)

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="/so-arm101/gifs/hero_st1_success.gif" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="/so-arm101/gifs/robot_d1_fails_st2.gif" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Left: a policy trained on single-sponge demos cleanly solves the single-sponge task. Right: the same policy trying a multi-sponge scene — it doesn't compose.
</div>

## How I got into this

[Prof. Mike Hagenow's CS839 — Topics in Advanced Robotics](https://wisc-rt2.github.io/cs839_spring26/) at UW–Madison handed each of us an SO-ARM101 — a low-cost 6-DoF arm from the [LeRobot](https://github.com/huggingface/lerobot) ecosystem — and a semester to do a project on it. I wanted to ask a specific question: **what does it actually take for an imitation-learning policy to generalize?**

The standard story is "more data, bigger model, better." I wanted to design something where I could isolate each of those axes — data composition vs. architecture vs. pretraining — and see which one mattered most for a kind of generalization I cared about: compositional generalization.

## The setup

I collected three pick-and-place datasets on the SO-ARM101:

- **T1: single sponge** — one blue sponge on the bench, pick and place in bowl.
- **T2: multi-sponge** — every blue sponge in the scene (1–6 per scene), pick all of them.
- **T3: clutter / distractors** — one blue sponge among visually-similar colored distractors.

128 episodes per task = 384 teleop demos total. Split 64 known-position / 64 random-position per task, plus four cross-task mixtures (D1+D2-Half, D1+D3-Half, D_D2D3, D_Universal) → **16 named datasets**.

Then I designed a **fourth evaluation task** — multi-sponge with distractors — and **never collected a single demo for it**. ST4 is the held-out compositional probe.

Trained three architectures on every relevant recipe:
- **ACT** (~84M params) — from scratch, no pretraining.
- **SmolVLA** (~450M) — Hugging Face's open VLA, full fine-tune of a SmolVLM-2 backbone.
- **Pi0.5** (~3.4B) — Physical Intelligence's VLA, VLM backbone frozen, only the action expert trains.

**39 trained policies, 684 scored real-robot rollouts, 202 GPU-hours over about a month** of iterating end-to-end (cloud compute donated by [CloudRift](https://cloudrift.ai)).

## Three things that surprised me

### 1. Compositional generalization isn't automatic

I expected a single-sponge policy to handle multi-sponge "for free" — humans who can pick one sponge can trivially pick several. LLMs that learn to add two numbers usually generalize to adding three. So this *felt* like it should compose.

It didn't. A policy trained on all 128 single-sponge demos scored 3.5/20, 2.5/20, and 7.0/20 on the multi-sponge task across ACT, SmolVLA, and Pi0.5. Adding just **64 multi-sponge episodes** to the mix jumped ACT to 18.5/20 and Pi0.5 to 17.0/20.

The held-out ST4 (multi-sponge + distractors) tells the same story even more cleanly: training on just two of the three source datasets dropped success from ~90% to ~50% on the same task. The policy needed every primitive to compose them.

### 2. Architectural differences only show up once you ask for compositional generalization

On ST1 and ST2 the three architectures look nearly identical when given the right data. They diverge sharply on ST3 and ST4. ACT scores 28/48 on ST3 and 17/20 on ST4. Pi0.5 scores 29/48 and 12/20. SmolVLA — the architecture that *should* benefit most from pretraining priors, given its size and recency — scores 10/48 and 6/20.

My hypothesis is that the ordering tracks **how each architecture treats its vision-language backbone during training**, not its parameter count:

- ACT has no VLM and trains its visual encoder from scratch on this dataset — specialized features.
- Pi0.5 keeps a large pretrained VLM **frozen** — strong priors preserved.
- SmolVLA **fully fine-tunes** a smaller VLM on a few hundred episodes — likely overwrites pretrained color/object semantics without enough data to rebuild them cleanly.

That's a hypothesis, not a controlled ablation. To prove it I'd need to train a frozen-backbone SmolVLA and a scratch-Pi0.5 — neither of which fit the semester budget.

### 3. The failure vocabulary shifts as the task gets harder

I tagged every one of the 684 rollouts inline with a failure-mode code via a custom iPad dashboard (G = grasp miss, C = wrong color/object, S = sequencing error, etc.). On the source tasks the bottleneck is almost entirely grasping. On ST4 it shifts dramatically to **color selection** — especially for Pi0.5, whose grasp:color failure ratio flips from 10:8 on ST3 to 1:6 on ST4.

This matters because it tells you distractor robustness is a *different capability* from clean pick-and-place — not just "more of the same." If you only measured success rate, you'd miss this entirely.

## What this isn't

Worth being upfront about the limits:

- **n = 8 known + 8 random trials per cell.** Some of the gaps between architectures are within sampling noise — single-trial-flip territory. The full report adds a Limitations section that's honest about this.
- **Single checkpoint per recipe.** I can't fully separate "Pi0.5 is worse on ST2" from "this Pi0.5 checkpoint happened to underconverge."
- **The vision-backbone hypothesis is post-hoc**, not a controlled ablation. It fits the data; a reviewer would want it isolated.
- **Compositional learning is not a new idea.** Open X-Embodiment, RT-2/RT-X, Pi0 itself, and a long line of skill-composition work have studied this. The interesting part of my project isn't *that* compositional generalization exists — it's the **clean 2×2 design** (object-count × distractor-presence) on a single arm where I could systematically vary data composition and architecture independently, and see which one moved the needle.

## Where to go from here

Full project page (with the interactive gallery streaming 661 rollouts from Hugging Face):
**[aswinkumar.me/so-arm101/](/so-arm101/)**

Code, data, and the iPad eval dashboard:
**[github.com/aswinkumar1999/so-arm101-imitation-learning](https://github.com/aswinkumar1999/so-arm101-imitation-learning)**

## Acknowledgements

Built on Hugging Face's [LeRobot](https://github.com/huggingface/lerobot) stack — thanks to the community for the policy implementations and dataset conventions. GPU compute donated by [CloudRift](https://cloudrift.ai) — the Blackwell access let me run 32 training jobs in parallel and stay in iteration mode instead of waiting on a queue. Huge thanks to [Prof. Mike Hagenow](https://www.hageneaux.com/) for the [course](https://wisc-rt2.github.io/cs839_spring26/), the framing, and the chance to work on this.

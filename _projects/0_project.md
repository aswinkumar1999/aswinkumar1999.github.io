---
layout: page
title: Data Composition vs Architecture in Robot Imitation Learning
description: Real-robot study on the SO-ARM101 comparing ACT, SmolVLA, and Pi0.5 across 16 dataset recipes and 684 scored rollouts
abstract: A 39-policy, 684-rollout real-robot study on the SO-ARM101 testing whether compositional generalization in imitation learning comes from architecture, pretraining, or training-data composition. Compares ACT (from scratch), SmolVLA (full fine-tune), and Pi0.5 (frozen VLM backbone) across 16 dataset recipes and a four-task family (single sponge, multi-sponge, distractor, multi-sponge + distractor). Headline finding — data dominates on the clean tasks; once distractors appear, architectures finally separate and the split tracks each model's vision-language-backbone treatment.
img: assets/img/project/so101.png
importance: 0
category: software
date: 2026-05-01
organization: University of Wisconsin-Madison
org_color: "#C5050C"
related_publications: false
---

<p align="center" style="font-size: 1.1em; margin: 1.5em 0;">
  <a href="https://aswinkumar.me/so-arm101/" style="font-weight: 600;">📄 Read the full project page →</a>
</p>

# Overview

CS839 "Topics in Advanced Robotics" final project (Prof. Mike Hagenow, UW–Madison, Spring 2026). On a single SO-ARM101 arm, this study asks when narrow-task training transfers to harder task variants — and how architecture and data composition interact to determine compositional generalization.

- **3 architectures**: ACT (~84 M params, trained from scratch), SmolVLA (~450 M, full fine-tune), Pi0.5 (~3.4 B, VLM backbone frozen).
- **4-task family**: ST1 single sponge → ST2 multi-sponge → ST3 clutter w/ distractors → ST4 multi-sponge + distractors (held-out).
- **16 dataset recipes**: known / random / mixed / combined per-task + cross-task half-mixes + universal.
- **684 scored real-robot rollouts**; 202 GPU-hours of training on cloud Blackwell + H200.

# Headline Findings

1. **Marked positions are a trap.** Known-only training overfits — ACT and SmolVLA both land at exactly 10/20 on ST1 from `D1-K`. Failure is in the data distribution, not the model class.
2. **Single-task training does not compose to multi-object (ST2).** D1-Combined → ST2 = 3.5/2.5/7.0 across the three archs; adding just 64 multi-sponge episodes (`D1+D2-Half`) jumps ACT to 18.5 and Pi0.5 to 17.0.
3. **Cross-task data helps.\*** ACT prefers distractor exposure; the two VLAs prefer multi-object exposure. Hypothesis: VLAs already have visual priors, so they benefit from extra grasping/sequencing — ACT trains its visual encoder from scratch and needs the distractor signal.
4. **Architectures emerge once distractors appear.** ST3/ST4 split the three: ACT and Pi0.5 stay competitive (28/48 and 29/48 on ST3), SmolVLA collapses (10/48). The ordering tracks how each architecture *treats* its vision-language backbone — scratch (ACT) and frozen (Pi0.5) preserve a competent visual representation; full-fine-tuning a smaller VLM on a few hundred episodes disturbs it without enough data to rebuild.
5. **Failure vocabulary shifts.** ST3 is grasp-heavy across the board; ST4 becomes color-selection-bound, sharpest for Pi0.5 (1:6 grasp:color). Distractor robustness is a distinct capability from clean pick-and-place.

# Artifacts

- **Project page (with embedded eval gallery):** [aswinkumar.me/so-arm101/](https://aswinkumar.me/so-arm101/)
- **Dataset (Hugging Face):** [aswinkumar99/LeRobot-SO101-Pick-Place](https://huggingface.co/datasets/aswinkumar99/LeRobot-SO101-Pick-Place)
- **Eval gallery videos (Hugging Face):** [aswinkumar99/so101-eval-gallery](https://huggingface.co/datasets/aswinkumar99/so101-eval-gallery)

# Acknowledgements

GPU compute donated by [CloudRift](https://cloudrift.ai). Built on the open-source [LeRobot](https://github.com/huggingface/lerobot) project. Course, feedback, and support by [Prof. Mike Hagenow](https://www.hageneaux.com/) and the [CS839 Spring 2026](https://wisc-rt2.github.io/cs839_spring26/) course at UW–Madison.

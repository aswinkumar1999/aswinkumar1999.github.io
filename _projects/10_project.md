---
layout: page
title: MABViT2 - Model Agnostic Bayesian Vision Transformer
description: Novel architecture for vision transformer with uncertainty quantification
abstract: Developed a model-agnostic Bayesian Vision Transformer that accurately quantifies uncertainty in predictions without requiring architectural changes. This approach extends Bayesian Deep Learning capabilities to Vision Transformers while maintaining predictive performance, addressing a critical need for reliable uncertainty estimates in high-stakes computer vision applications.
importance: 10
category: software
date: 2023-09-01
organization: University of Wisconsin-Madison
org_color: "#C5050C"
related_publications: false
---

# Project Overview:

Vision Transformers (ViTs) have emerged as powerful models for computer vision tasks but often lack reliable uncertainty quantification. This project addresses this gap by developing MABViT2, a Model Agnostic Bayesian Vision Transformer, enabling uncertainty estimation without architectural modifications.

# Key Contributions:

- Developed a Bayesian ViT model that quantifies uncertainty without architectural changes
- Implemented a variational inference approach for parameter estimation
- Validated performance on benchmark datasets while maintaining competitive accuracy
- Demonstrated superior out-of-distribution detection compared to deterministic baselines
- Created a flexible implementation that can be applied to any existing Vision Transformer

# Technical Details:

The MABViT2 framework uses a Monte Carlo Dropout method in the self-attention mechanism to approximate Bayesian inference. By running multiple forward passes with different dropout masks, the model generates a distribution of predictions that capture epistemic uncertainty. The implementation is compatible with existing ViT architectures like DeiT and ViT-B models.

# Significance:

This work bridges a critical gap in computer vision by enabling uncertainty quantification in transformer-based models, which is essential for high-stakes applications like medical imaging and autonomous driving. The model-agnostic approach makes it straightforward to apply to existing systems without architectural redesign.
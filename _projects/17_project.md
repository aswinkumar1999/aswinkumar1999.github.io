---
layout: page
title: Cheetah Soft Robotics Simulator
description: Simulation platform for soft robots with real-time performance using GPU acceleration
abstract: Developed a specialized simulation platform for soft robotics focusing on bio-inspired designs like a cheetah robot with flexible spine. The simulator features a novel FEM-based deformation model with GPU acceleration, achieving real-time performance while accurately capturing the complex dynamics of soft and hybrid rigid-soft robotic systems, enabling both controller design and morphological optimization.
importance: 17
category: software
date: 2021-12-01
organization: IIT Madras
org_color: "#231f7e"
related_publications: false
---

# Project Overview:

This project addresses the challenge of efficiently simulating soft and hybrid rigid-soft robots for design and control applications. Inspired by biological systems like cheetahs, which use their flexible spine for enhanced locomotion, the simulator enables exploration of bio-inspired designs that incorporate soft, deformable components alongside traditional rigid elements.

# Key Features:

- FEM-based deformation model for accurate simulation of soft materials with varying properties
- GPU-accelerated parallel solver achieving real-time performance for complex models
- Unified treatment of rigid and soft body dynamics within a single simulation framework
- Contact model specifically designed for soft-rigid interactions
- Open-source implementation with Python and C++ APIs

# Technical Implementation:

The core of the simulator is built on a finite element method (FEM) approach using a corotational formulation for large deformations. To achieve real-time performance, the computational bottleneck of solving large sparse linear systems is addressed through a custom GPU-accelerated preconditioned conjugate gradient solver.

The system incorporates a unified constraint-based formulation that handles both soft body deformation and rigid body dynamics, allowing for seamless simulation of hybrid systems. A specialized contact model accounts for the unique challenges of soft material contact, including friction and self-collision.

# Applications:

The simulator has been applied to several bio-inspired robotic designs, including:

1. **Cheetah-inspired robot**: A quadrupedal robot with a flexible spine, demonstrating how controlled spinal flexibility can enhance running efficiency and maneuverability.

2. **Soft grippers**: Simulation of pneumatically actuated soft grippers for delicate object manipulation.

3. **Tensegrity robots**: Robots that use a combination of rigid struts and flexible tensile elements for locomotion and adaptation.

# Impact:

The simulator enables researchers to explore the design space of soft and hybrid robots more efficiently, testing concepts virtually before physical prototyping. The ability to run simulations in real-time facilitates the development of control algorithms and the application of learning-based approaches to this challenging domain.
---
layout: page
title: Robot Action Exploration using Bayesian Optimization
description: Novel reinforcement learning approach for efficient robot skill acquisition
abstract: Developed a hierarchical exploration strategy for robot manipulation tasks using Bayesian optimization and directed exploration. This approach enables robots to efficiently learn complex manipulation skills with minimal human supervision by balancing exploration and exploitation in a structured action space, resulting in 45% faster skill acquisition compared to standard reinforcement learning methods.
importance: 13
category: software
date: 2023-05-01
organization: University of Wisconsin-Madison
org_color: "#C5050C"
related_publications: false
---

# Project Overview:

This project addresses the challenge of efficient exploration in robotic manipulation tasks. Traditional reinforcement learning approaches often struggle with the high-dimensional action spaces and sparse rewards common in manipulation tasks. Our approach uses Bayesian optimization to guide exploration in a hierarchical action space, significantly improving learning efficiency.

# Key Contributions:

- Developed a hierarchical exploration strategy that decomposes complex manipulation tasks into subtasks
- Implemented a Gaussian Process-based Bayesian optimization framework for efficient action selection
- Created a directed exploration mechanism based on information gain and expected improvement
- Designed a task-agnostic representation that generalizes across different manipulation scenarios
- Evaluated the approach on a range of real-world robotic manipulation tasks

# Technical Implementation:

The framework consists of three main components:

1. **Hierarchical Action Space**: Complex manipulation tasks are represented as sequences of primitive actions organized in a hierarchical structure.

2. **Bayesian Optimization**: A Gaussian Process model maintains a belief over the reward function, guiding exploration toward promising regions of the action space.

3. **Information-Directed Sampling**: Actions are selected based on a combination of expected reward and information gain, balancing exploration and exploitation.

The system was implemented using PyTorch for the learning components and integrated with ROS for robot control. Experiments were conducted on a 7-DOF robotic arm performing various manipulation tasks.

# Results:

- 45% faster skill acquisition compared to standard reinforcement learning approaches
- Successful learning of complex manipulation tasks with as few as 50 physical trials
- Effective transfer learning between related tasks
- Robust performance under varying initial conditions and object properties

The approach demonstrates significant potential for enabling robots to autonomously learn manipulation skills with minimal human supervision, a critical capability for deploying robots in unstructured environments.
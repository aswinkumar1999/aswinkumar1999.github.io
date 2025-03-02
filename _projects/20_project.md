---
layout: page
title: Autonomous UAV Navigation System
description: Vision-based navigation system for drones operating in GPS-denied environments
abstract: Developed a complete autonomous navigation system for unmanned aerial vehicles (UAVs) capable of operating in GPS-denied environments using only onboard sensors. The system integrates visual-inertial odometry, SLAM, and learning-based obstacle avoidance to enable robust flight in challenging indoor and outdoor environments, with successful demonstrations in search and rescue scenarios, infrastructure inspection, and warehouse inventory management.
importance: 20
category: software
date: 2020-08-01
organization: IIT Madras
org_color: "#231f7e"
related_publications: false
---

# Project Overview:

This project addresses the challenge of enabling autonomous UAV operation in environments where GPS signals are unavailable or unreliable. By relying solely on onboard sensing and computing, the system provides robust navigation capabilities for applications including search and rescue, infrastructure inspection, and indoor operations.

# Key Features:

- Visual-inertial odometry for accurate state estimation without GPS
- Real-time 3D mapping and simultaneous localization (SLAM)
- Learning-based obstacle detection and avoidance
- Path planning with dynamic obstacle handling
- Fault-tolerant control system with emergency recovery modes
- Lightweight implementation suitable for deployment on commercial drones
- Development of a custom simulation environment for testing and validation

# Technical Implementation:

The system consists of four main components:

1. **Perception**: A visual-inertial odometry pipeline fuses data from stereo cameras and an IMU to estimate the drone's position and orientation. This is complemented by a lightweight SLAM system that builds and maintains a 3D map of the environment.

2. **Obstacle Avoidance**: A deep learning-based approach detects obstacles from camera images, while a secondary system uses depth information for obstacle verification. The combined system provides reliable obstacle detection even in challenging lighting conditions.

3. **Planning**: A hierarchical planning system combines global path planning using a topological map with local trajectory optimization that accounts for dynamics constraints and obstacle avoidance.

4. **Control**: A robust control system translates planned trajectories into motor commands, with adaptive gains to handle different flight conditions and failure modes.

The entire system runs on an NVIDIA Jetson Xavier NX onboard computer, with a custom software stack developed using ROS and optimized for real-time performance.

# Applications and Results:

The system has been successfully deployed in several applications:

- **Search and Rescue**: Autonomous exploration of disaster sites with detection of victims using thermal imaging
- **Infrastructure Inspection**: Automated inspection of bridges and buildings with detailed 3D reconstruction
- **Warehouse Inventory**: Indoor navigation for inventory tracking and management

Performance metrics demonstrate:
- Localization accuracy of ±5cm in controlled environments
- Obstacle detection range of up to 10m with 95% accuracy
- Successful navigation through complex environments with doorways and corridors
- Flight endurance of 15 minutes with full autonomy stack active
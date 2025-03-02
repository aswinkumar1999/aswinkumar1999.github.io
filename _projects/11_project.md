---
layout: page
title: Autonomous Hexapod Robot
description: Designed and built a six-legged robot with advanced locomotion capabilities
abstract: Created a fully autonomous hexapod robot with distributed control architecture enabling dynamic stability and advanced terrain navigation. The robot features custom-designed PCBs for motor control, onboard computer vision, and an adaptive gait generator that dynamically adjusts to environmental challenges, allowing for smooth operation over varied terrain.
img: assets/img/project/hexapod.jpg
importance: 11
category: hardware
date: 2020-12-01
organization: IIT Madras
org_color: "#231f7e"
related_publications: false
---

# Project Overview:

This project involved designing and constructing a six-legged robot (hexapod) with autonomous capabilities. The hexapod features a distributed control system architecture where each leg has independent control while a central controller coordinates overall movement patterns and stability.

# Key Features:

- Six-legged design with 3 degrees of freedom per leg (18 actuated joints total)
- Custom-designed PCBs for motor control and power distribution
- Implemented advanced gait generation algorithms for different terrain types
- Developed a real-time stability management system using accelerometer and gyroscope data
- Integrated computer vision for obstacle detection and navigation planning
- Designed a lightweight but durable chassis using 3D-printed components

# Technical Implementation:

The robot uses a hierarchical control system with an ARM Cortex-M4 microcontroller as the main controller and dedicated controllers for each leg. Communication between controllers happens over a custom real-time protocol. The gait generator implements several locomotion patterns including tripod, wave, and ripple gaits that can be switched dynamically based on terrain.

A RaspberryPi handles higher-level functions including computer vision through a Pi Camera module, processing images to detect obstacles and plan navigation paths. The power system features lithium polymer batteries with efficient DC-DC conversion to maximize runtime.

# Applications:

The hexapod platform demonstrates capabilities relevant to search and rescue operations, exploration of hazardous environments, and as an educational platform for robotics research. Its ability to navigate uneven terrain makes it suitable for applications where wheeled robots would struggle.
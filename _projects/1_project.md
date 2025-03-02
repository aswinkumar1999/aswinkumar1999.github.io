---
layout: page
title: DCT and IDCT Hardware Accelerator
description: Hardware implementation of Discrete Cosine Transform (DCT) and its inverse for signal processing applications
abstract: A high-performance hardware accelerator designed for the efficient computation of DCT and IDCT operations, key components in modern compression algorithms. The accelerator leverages a novel pipelined architecture with butterfly computation units to achieve throughputs suitable for real-time processing of HD video content while maintaining low power consumption.
img: assets/img/project/IDCT.png
importance: 1
category: hardware
date: 2022-05-01
organization: NVIDIA
org_color: "#76b900"
related_publications: true
---

This project implements a hardware accelerator for Discrete Cosine Transform (DCT) and Inverse Discrete Cosine Transform (IDCT) for signal processing and media applications. 

<div class="row"> <div class="col-sm mt-3 mt-md-0"> {% include figure.liquid loading="eager" path="assets/img/project/dct.png" title="DCT Diagram" class="img-fluid rounded z-depth-1" %} </div> <div class="col-sm mt-3 mt-md-0"> {% include figure.liquid loading="eager" path="assets/img/project/IDCT.png" title="IDCT Diagram" class="img-fluid rounded z-depth-1" %} </div> </div> <div class="caption"> Left: Flow graph of DCT. Right: Flow graph of IDCT. </div>

# Project Overview:

The core of this work is to implement a hardware accelerator for DCT and IDCT, which are crucial in various signal processing and media applications. With the growth of information technology, the need for efficient compression algorithms has become paramount. DCT has been widely used for several decades due to its incredible energy compaction properties.
This project focuses on implementing hardware-level DCT and IDCT transforms for energy-efficient encoding and decoding. The implementation is done using Bluespec, a high-level hardware description language. 

# Key Features: 

- Implementation of Fast DCT algorithm
- Implementation of IDCT algorithm
- Modular design for 4-point, 8-point, 16-point, and 32-point transforms
- Use of Butterfly and Hadamard modules for efficient computation
- Pipelined architecture for higher throughput
- The project demonstrates the potential for hardware acceleration in signal processing tasks, particularly in the context of media compression and decompression. It provides a foundation for further optimization and integration into larger systems dealing with video and image processing.
---
layout: note
title: "LLM Pre-training and Scaling Laws"
date: 2026-10-27
category: gen-ai
pdf: "/assets/notes/LLM pre-training and scaling laws.pdf"
pages: 4
description: "Notes on LLM pre-training pipelines, multi-GPU distributed training with DDP vs. FSDP, Chinchilla scaling laws, and pre-training for domain adaptation."
---

> **Disclaimer**: These notes are intended solely for personal study and reference; they are not detailed or exhaustive, and are not for any monetary or commercial use. Any images or conceptual diagrams referenced belong to DeepLearning.AI.

These notes cover core concepts in training large language models:

- **Multi-GPU Distributed Training**: When models fit on a single GPU vs. when parameters exceed single-GPU memory.
- **Distributed Data Parallel (DDP)**: Parameter replication, parallel forward passes, backpropagation, and gradient all-reduce synchronization.
- **Fully Sharded Data Parallel (FSDP)**: Sharding model parameters, gradients, and optimizer states across GPUs; layer-by-layer parameter gathering during forward and backward passes.
- **LLM Scaling Laws**: Chinchilla compute-optimal training (~20 tokens per parameter).
- **Pre-training for Domain Adaptation**: Adapting LLM vocabularies and weights to niche domains (e.g., BloombergGPT trained on 51% financial and 49% public data).

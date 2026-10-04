---
layout: note
title: "Sequence Modelling: RNNs, GRUs & LSTMs"
date: 2026-10-10
category: deep-learning
pdf: "/assets/notes/Sequence modelling GRUs,RNNs & LSTMs.pdf"
pages: 64
description: "Handwritten notes on sequence modelling: recurrent neural networks, vanishing gradients, GRU and LSTM gating mechanisms, and bidirectional architectures."
---

These notes cover architectures designed for sequential and temporal data:

- **Recurrent Neural Networks**: Hidden state propagation, unrolling through time, and backpropagation through time (BPTT).
- **Vanishing & Exploding Gradients**: Why vanilla RNNs struggle with long sequences and how gating solves it.
- **LSTM**: Forget gate, input gate, output gate, cell state — the full gating mechanism explained visually.
- **GRU**: Simplified gating with reset and update gates, and comparison with LSTM.
- **Bidirectional RNNs**: Processing sequences in both directions for richer context.

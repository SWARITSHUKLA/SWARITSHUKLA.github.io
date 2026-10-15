---
layout: note
title: "Basics of Training Optimization"
date: 2026-10-13
category: systems
description: "Training optimization fundamentals — efficient training pipelines, hardware utilization, and performance tuning."
---
> This note is from the Andrej Karpathy lecture on GPT-2 and i would higly recommend watching that, i am writing this because its padagogically the best way to learn, the best way for you to learn from this article is to copy paste the entire thing, give it an LLM and ask for explanation :)

## Quantization 

### NVIDIA B100 Tensor Core GPU Specifications

| Specification | NVIDIA B100 |
|---|---:|
| FP64 | 30 TFLOPS |
| FP64 Tensor Core | 30 TFLOPS |
| FP32 | 60 TFLOPS |
| TF32 Tensor Core | 0.9 PFLOPS / 1.8 PFLOPS* |
| FP16 Tensor Core | 1.75 PFLOPS / 3.5 PFLOPS* |
| BF16 Tensor Core | 1.75 PFLOPS / 3.5 PFLOPS* |
| FP8 Tensor Core | 3.5 PFLOPS / 7 PFLOPS* |
| FP6 Tensor Core | 3.5 PFLOPS / 7 PFLOPS* |
| FP4 Tensor Core | 7 PFLOPS / 14 PFLOPS* |
| INT8 Tensor Core | 3.5 POPS / 7 POPS* |
| GPU Memory | 192 GB HBM3e |
| GPU Memory Bandwidth | 8,000 GB/s (8 TB/s) 

" * with sparsity "

Here is what we can infer from the table above that shows the performance given the quantization of the tensors,

- When you decrease the precision of the tensor cores the models performance improves a lot for example going from $FP32$ to $BF16$ we get a performance improvement.

The peak BF16 Tensor Core performance is:

$$
1.75 \text{ PFLOPS} = 1750 \text{ TFLOPS}
$$

The theoretical speedup is:

$$
\text{Speedup} = \frac{\text{BF16 Performance}}{\text{FP32 Performance}}
= \frac{1750}{60}
\approx 29.17\times
$$

Therefore, the NVIDIA B100's peak BF16 Tensor Core throughput is approximately 29.17 times its peak standard FP32 throughput.

> Note: This compares theoretical peak throughput, not actual application speed. The observed speedup depends on the workload and hardware utilization, GPUs can perform calculations superfast but they are still memory bound so it will still take time for data to travel from HBM to GPU, if you want to read more about the it you can read this article that i wrote - [Batch Size and LLM Inference Efficiency](https://swaritshukla.me/deep-ai/2026/07/21/Batch-Size-and-LLM-Inference-Efficiency.html).

| Format | Sign Bits | Exponent Bits | Fraction (Mantissa) Bits | Total Bits |
|:-------|:---------:|:-------------:|:------------------------:|:----------:|
| FP32   | 1         | 8             | 23                       | 32         |
| BF16   | 1         | 8             | 7                        | 16         |

The difference between FP32 and BF16 is the precision used, both of them have same number of exponent bits meaning the range remains same but Mantissa bits decreases in BF16 making it less precise. We dont need very high precision in deep learning so we can work with less precision without sacrificing a lot on performance.

- we can go even low while doing the inference upto INT8 Tensor Core and still get some reasonable results
 
- different component of the model can use different kind of precision, the attention layers and other non-expert components can use higher precision, while the enormous MoE expert weights may use less precision like MXFP4

### Why range matters more than precision 
We dont need bfloat16 to represent parameters that are huge for example a parameter will never be of value $10^8$, We need it while doing doing the forward/backward pass where numbers can become fairly large, for example 
$y = w_1x_1 + w_2x_2 + \cdots + w_nx_n$ can become a pretty huge number and to represent that we need a big range.

## Compiling the model 
Once you define a model you have to to now run it and. Python executes the model's operations and dispatches them to the CPU or GPU. This introduces some overhead, Specially when a model has a lot of small operations to perform, We can reduce this overhead using torch.compile(), This creates an instance of the compiled version of the model which has less python overhead, it captures models computaattion and optimizes it.

```python
model = torch.compile(model)
```

PyTorch uses TorchDynamo to capture the computation graph and TorchInductor to generate optimized code for execution, it combines multiple small operations into fewet GPU kernels.

Using torch.compile() comes at the cost of initial overhead where pytorch compiles the model before executing its optimized version.

It uses openAIs Triton under the hood to generate GPU kernels for NVIDIA's GPUs, torch.compile() isnt availible for MPS as of now (5 oct 2026).

### Kernel fusion 
A kernel is a function that runs on GPU and performs a specific computation, so lets say you have to use a function with multiple intermediate calculations, The memory bandwidth bandwidth overhead is going to be huge the GPU will have to fetch the data from HBM and then it would perform one of that intermediate computation send the Data back to HBM, It will fetch the data again from the HBM perform another intermediate calculation till the whole calculation is finished.

To counter this specific problem we use Kernel fusion where we add multiple kernel operatioins into one kernel and perform the computation which decreases the memory bandwidth overhead and makes computation significantly faster. 

The best example of this is Flash attention.
Where we fuse the whole attention mechanism calculations into one kernel function and it reduces the latency.

## Nice numbers
The numbers which are in the power of 2 are considerd nice numbers

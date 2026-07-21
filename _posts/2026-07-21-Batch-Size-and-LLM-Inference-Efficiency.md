---
layout: post
title: "Batch Size and LLM Inference Efficiency"
date: 2026-07-21
category: deep-ai
---
Having an optimal Batch size can decrease your models cost per token at the time of inference.

This will be an explanation on how Batch size effects the cost at the inference, We will be going deep and building the framework from the ground up. this will be an informal explanation of the concept so dont expect any formal language. 

Shall we begin this journey my square. 

## Dependencies 
So first thing we need to understand is what does LLM inference actualy depends upon. 

![equation 1](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/art%201.jpeg)

In the equation above we can see that the actual time taken to do inference depends on two major factors 

1 -> Memory 

    
    KV cache & Model weights fetching time 

2 -> Compute 

    The time it takes to perform mathematical operations 

The equation says, The time it takes to do inference is greater than or equal to the max value between time it takes for compute and time it takes to fetch the memory.
### Time taken to fetch the memory ($t_{memory}$)
![equation 2](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/art%204.jpeg)

In the equation above, time taken to fetch the memory is the sum of size of the model in bytes and the kv cache in bytes divided by the memory bandwidth

here the kv cache is

$B \cdot \text{len}_{\mathrm{ctx}} \cdot \left(\frac{\text{bytes}}{\text{token}}\right)$

### Time taken for compute ($t_{compute}$)
![equation 3](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/art%202.jpeg)
The equation $t_{compute}$ is batch size multiplied by number of active parameter divided by flops 

We dont take time it takes to do the attention computation into accounts because its trivial when you compare it with the weight matrix multiplication cost.
![equation 4](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/art%203.jpeg)

## Plotting the graphs 
What we have here is the latency plot, we are essentially plotting all the values that we worked with earlier, on this graph.

    plot 1.1 

![equation 4](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.1.jpeg)
- $t_{compute}$ grows linearly as the batch size increases
- $t_{kv-fetch }$ also grows linear. 
- $t_{weight-fetch }$ dosent grow at all it remains constant
---

    plot 1.2 
    
 ![equation 4](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.2.jpeg)
 - plotting the conjuntion of both $t_{weight-fetch }$  & $t_{kv-fetch }$ as $t_{memory}$
 - notice that the y intercept of $t_{memory}$ starts exactly from the  $t_{weight-fetch }$ intercept
---
    plot 1.3
 ![equation 4](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.3.jpeg)
 - Here we are taking the maximum of $t_{compute}$ & $t_{memory}$
 - Now this graph tells us, How latency grows with the increase in batch size 
 



 
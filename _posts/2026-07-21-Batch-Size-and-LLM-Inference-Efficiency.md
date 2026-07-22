---
layout: post
title: "Batch Size and LLM Inference Efficiency"
date: 2026-07-21
category: deep-ai
---
Having an optimal Batch size can decrease your models cost per token at the time of inference.

This will be an explanation on how Batch size effects the cost at the inference, We will be going deep and building the framework from the ground up. this will be an informal explanation of the concept so dont expect any formal language. 

> The word plot and graph are used interchangebly in this Article so dont get confused

Shall we begin this journey my square. 

![ser dunken the tall and egg](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/Dunk-and-Egg.jpg)

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

![plot 1.1](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.1.jpeg)
- $t_{compute}$ grows linearly as the batch size increases
- $t_{kv-fetch }$ also grows linear. 
- $t_{weight-fetch}$ dosent grow at all it remains constant

---

    plot 1.2 
    
 ![plot 1.2](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.2.jpeg)
 - plotting the conjuntion of both $t_{weight-fetch }$  & $t_{kv-fetch }$ as $t_{memory}$
 - notice that the y intercept of $t_{memory}$ starts exactly from the  $t_{weight-fetch }$ intercept

---

    plot 1.3

 ![plot 1.3](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%201.3.jpeg)

 - Here we are taking the maximum of $t_{compute}$ & $t_{memory}$
 - Now this graph tells us, How latency grows with the increase in batch size.
 - The point worth noting here is that there is a lower bound on latency, because the time it takes to load the model parameters is a constant

> we have been plottng the latency (***t***) as the function of batch size, but to get cost per token we need to plot (***t/B***) cost as the fucntion of batch size.

---

    plot 2.1
 
![plot 2.1](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%202.1.jpeg)

The Graph 2.1 plots (***t/B***) as a function of (***B***), and the variables change quite a bit 

- $t_{compute}$ was linear but after dividing it by (***B***) we get a constant 
- $t_{KV-fetch}$ was also linear but after dividing it by (***B***) we get a constant 
- $t_{weight-fetch}$ was constant but after dividing it by (***B***) we get a hyperbolic curve

---

    plot 2.2

![plot 2.2](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%202.2.jpeg)

 - Plotting the conjuntion of both $t_{weight-fetch }$  & $t_{kv-fetch }$ as $t_{memory}$
 - What happens is that the conjuntion shifts the parabola up

 ---

    plot 2.3

![plot 2.3](/photos/Batch%20Size%20and%20LLM%20Inference%20Efficiency/graph%202.3.jpeg)

- Taking the maximum of the graph 2.2 we get graph 2.3 
- Now, you can see the cost per token plot 

### Observations 

- In the graph 2.3 you can see that the cost decreases as we increase the batch size until it hits the lower bound 
- If you want you can do a cost and inference time tradeoff where as you decrease the batch size the cost goes up but inference time decreases
- There is a lower bound on cost too which is $t_{compute}$.
- Here is a caveat, As you increaase the batch size, at some point $t_{kv-fetch }$ will surpass $t_{compute}$ and at that point compute is no longer the lower bound its memory bandwidth and the MFU (model flop utilization) decreases significantly, So the cost/token increases if the batach size is too big 

Thanks for the read :)

I wrote this article becasue its the most pedagogically effective way for me to understand this topic explained by Reiner Pope on [Dwarkesh patel](https://www.youtube.com/watch?v=xmkSf5IS-zw&t=160)
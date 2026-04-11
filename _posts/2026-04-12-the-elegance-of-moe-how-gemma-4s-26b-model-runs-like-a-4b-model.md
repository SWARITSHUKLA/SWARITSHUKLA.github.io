---
layout: post
title: "The Elegance of MoE: How Gemma 4's 26B Model Runs Like a 4B Model"
date: 2026-04-12
---

![Gemma 4 Architecture Outline](/photos/gemma-4_Title%20image.webp)
Google recently dropped its new family of open-source AI models, **Gemma 4**, but the variant that truly captured my interest is **Gemma-4-26B-A4B-IT**. The question is: how can a 26 billion parameter model only activate 4 billion parameters at a time? This is where the elegance lies. By only activating 4 billion parameters, it reduces the cost of compute a lot. So what’s the magic behind this? It turns out it uses a clever architecture called MoE (Mixture of Experts) that lets the model choose experts, and hence it only activates 4 billion parameters, making it extremely fast and compute-efficient.

A Mixture of Experts model is not a giant monolith. Internally, it is divided into experts (for example, 128). Experts specialize in different fields like coding, physics, calculus, and literature. So instead of using a giant neural network, it uses smaller expert neural networks. Note that these experts are not predefined—the neural network learns this itself during backpropagation.

## Dense models vs Mixture of Experts

Traditional dense models differ from Mixture of Experts. In a dense model, each input token is fed to all of the parameters—but not in the case of MoE.

MoE uses a router that assigns a token to only the **top k** experts (usually 2 or 8). The router (which is a neural network) takes in the token as input and then computes probabilities for all the experts. The top two with the highest probability are assigned that token.

So at a time, only four billion parameters are activated, and the remaining 22 billion sit idle.

![Gemma 4 Benchmarks](/photos/gemma-4-benchmarks.jpg)

## The restaurant analogy

Think of it this way—there are two restaurants:

**1. Dense restaurant**  
You place an order.  
In a dense restaurant, that order gets passed to every chef, and every chef works on it. It doesn’t matter if the order is for pasta—even the dessert chef will work on it. After every chef works on the dish, they create a delicious pasta.

**2. MoE restaurant**  
This is where the router—the manager of experts—comes into play.

In an MoE, instead of the order directly going to the chefs, it first goes to the manager. The manager then decides which two chefs will work on the dish. If the dish ordered is pasta, then the two chefs working on it would be:

1.  **The Vegetable Chef (Entremetier):** Boils the starch (the pasta noodles)
2.  **The Sauce Chef (Saucier):** Cooks the hot, savory meat sauce to pour over the top

Together, they create a delicious pasta without making all the chefs in the restaurant work on it. It’s as good as the one made by a dense restaurant, but with fewer chefs involved.

(The idea for this analogy came from _The Bear_ show—it’s an amazing show, by the way. Check it out.)

## Total vs Active parameters

**Total parameters** – This represents the amount of diverse knowledge an LLM has. Let’s say a model has 128 experts and 26 billion parameters. Those 26 billion parameters are spread across 128 experts in their fields. Some are good at math, some at literature, and they might also go niche—like an expert in pop culture, movies, and music.

**Active parameters** – This represents the compute cost of the model. So if a model has 26 billion parameters but only activates 4 billion at a time, the model’s compute cost and response time become that of a 4 billion parameter model.

## The vRAM twist

Even though the model becomes extremely efficient at generating inference and reduces the compute cost significantly, there’s still the angle of vRAM.

It doesn’t matter if the model activates only 4 billion parameters at a time—you still have to load the whole 26 billion parameters into your vRAM. So even though your low-end hardware can run the model efficiently, to load the model you will still need enough vRAM, which may force you to use a high-end system.

It might give you fast responses and consume less energy, but you will still need a powerful device.

## An intuitive demonstration

Let’s say you input the sequence: **"Indian cuisine is very..."** and the LLM has to complete it.

1.  **Input** – The token "Indian" arrives
2.  **Router’s evaluation** – Based on mathematical evaluation of the token "Indian", the router selects the top 2 experts, which could be the ones that specialize in geography (#34) and food (#87). (Modern LLMs consist of multiple layers stacked together, so the router assigns the token to different experts repeatedly as it goes deeper into the architecture.)
3.  **Computation** – Only the parameters in experts #34 and #87 get activated and used for computation, while the remaining parameters stay idle
4.  **Repetition** – The model repeats the process, but this time the router might choose completely different experts based on the next token

## The History

It might seem like a very novel idea to most people, but the actual concept was introduced more than three decades ago, in 1991, by Robert A. Jacobs, Michael I. Jordan, Steven J. Nowlan, and the "Godfather of AI," **Geoffrey E. Hinton**. The paper was titled _"Adaptive Mixtures of Local Experts."_

The modern implementation of this idea came in 2017. The paper, titled _"Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer,"_ was written by Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean (the Google Brain team). This paper further refined the idea by introducing the concept of sparsity—it forced the neural network to activate only a small number of parameters at a time, making them highly efficient.

----------

**by Swarit Shukla**
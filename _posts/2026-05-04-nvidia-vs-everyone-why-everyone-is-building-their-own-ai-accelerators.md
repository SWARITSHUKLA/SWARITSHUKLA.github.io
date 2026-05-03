---
layout: post
title: "Nvidia Vs Everyone: Why everyone is building their own accelerators"
date: 2026-05-04
category: ai-hype
---

There has been a race in the AI industry to generate custom AI accelerators, companies are now preferring their own custom accelerators to train AI models and generate inference from them. But why? Why all of a sudden is everyone ditching Nvidia and either building their own accelerators or just buying from the ones that make them? For example, Anthropic uses Google's TPUs (Tensor Processing Units), Amazon is offering their own Trainium chips, and OpenAI is hinting at making their own custom accelerators. The answer is fairly simple, and it's not because they don't want Nvidia to dominate over the market; it's because their accelerator chips are faster than those Nvidia GPUs. So, let's discuss this in detail.

![Jensen Nvidia vs everyone photo](/photos/jensen_Nvidia%20%20vs%20everyone%20photo.webp)

## Why is everyone building their own accelerators?
Nvidia has a reputation of making the best accelerated computing chips in the world, and for a long time everyone used them, but in recent years we are seeing a shift from GPUs to ASICs (Application-Specific Integrated Circuits).

Once an AI model has been trained, running and constantly generating inference from it using GPUs is not very economical. The cloud service providers and hyperscalers are looking for custom chips that strip away the unnecessary components of GPUs, handling only a specific work, hence reducing the TCO (Total Cost of Ownership).

The current data centers are power-hungry; they consume multiple gigawatts of power. Many CEOs, including Sam Altman, say that power is the ultimate bottleneck for AI. So to minimize power consumption, companies are turning to ASIC chips which increase performance per watt.

Companies want control on their hardware; relying solely on Nvidia means fighting for the GPUs and waiting in the queue. By having their own chips, they are simply reducing their dependency on Nvidia.

# The difference between general purpose accelerators and application-specific accelerators

You can say that AI models are just mathematical equations, so when we say transformer architecture, we are just referring to a sequence of mathematical operations that approximately looks like:
* Multiply matrices (weights and input)
* Add some numbers (bias)
* Run softmax (a mathematical function)
* Move to the next layer

### How a general purpose accelerator handles it: 
A general purpose accelerator doesn't have any idea what a transformer architecture looks like; it just knows how to do basic maths. So it fetches the instructions to follow, it looks like: 
* Check the memory for instructions (it says multiply)
* Get number a and b from the memory 
* Send them to the calculator unit 
* Save the answer back to the memory
* Check the memory for the next instruction 

Most of the energy is spent moving data between memory and compute, including reading instructions.

### How an ASIC handles it:
We already know what maths is coming in the sequence so we don't need to fetch instructions and move data in and out of the memory, so they take the physical logic gates that multiply matrices and connect their output to the logic gates that do softmax.

In ASIC chips there is no instruction reading. The data enters and the laws of physics force it to go through a set sequence that generates the output.

It's like an automated car wash, you just take the car in and a clean car comes out. No interventions are being made, no directions are given, just the car goes in and comes out clean.

## How is Nvidia different from others?
Nvidia's biggest moat isn't their chip designs, it's "CUDA" and "SUPPLY CHAIN".

CUDA stands for Compute Unified Device Architecture. It's a parallel computing platform that enables developers to use any CUDA-enabled GPU as a general purpose computing device. Millions of developers write software for CUDA; if you wrote a piece of software and it works on your Nvidia GPU, then it will surely work on any NVIDIA GPU. 

So if you are a startup writing code for Nvidia GPUs, you instantly unlock the deployment for every cloud service because every cloud service company in the world runs Nvidia GPUs.

While watching the Jensen Huang podcast with Dwarkesh Patel, I realized that Nvidia has invested heavily to eradicate the bottlenecks. They determine bottlenecks in the supply chain prior, and go all in to make sure that it doesn't bother them.

They have invested heavily in CoWoS packaging technology, silicon photonics (interconnects using light), and HBM (High Bandwidth Memory). Nvidia handles the upstream very well so that it can stay ahead of the competition.

## Why are Nvidia's chips still better than ASIC chips?
When you compare an ASIC with accelerators, on paper surely you will see ASICs outperforming Nvidia's accelerators, but in real life that's not the case. Nvidia accelerators give the best performance per watt in today's time.

Nvidia doesn't just sell the accelerators and rest, they have a lot of high-performing software engineers that continuously optimize the lowest-level code that runs on the accelerators. Nvidia helps the companies to optimize their code so they can run super fast on their GPUs.

Jensen, while on the podcast with Dwarkesh Patel, gave a very good analogy. He said anyone can drive an F1 car, but to push it to its absolute limits you need to have a lot of expertise. He was referring to F1 cars as his accelerators here; they send their best software engineers to the AI labs and optimize their software so that it runs best on Nvidia hardware.

Here is the most important point: the bottleneck is not the chip, it's the network. Modern AI models are not trained and run using a single chip; they are trained and run on multiple chips working together. So it doesn't matter if your chip is super fast because most of the time it will be sitting idle and waiting for the data to arrive. Nvidia recognized this bottleneck a long time ago and acquired Mellanox, a company that builds high-speed networking. Nvidia builds NVLink switches and InfiniBand networking fabrics that connect them.

I would encourage you to think of Nvidia not as a chip design company but as a "DATACENTER MAKING COMPANY".

## Why isn't Nvidia making ASIC chips?
So here is the real question: if NVIDIA can design the best chips and has got the best networks, then why aren't they making ASIC chips themselves? 

To answer this question let me ask you a different question. We know that ASIC chips are hardwired to follow a specific sequence of maths and give the output, but what if the fundamental architecture behind the AI models (which is Transformers) changes? The answer is those ASIC chips instantly go from accelerators to paperweights; they will not be able to perform computation because the architecture has been changed and the chips are hardwired to perform computation for a specific architecture.

The total addressable market (TAM) is bigger for general purpose accelerators. If NVIDIA builds ASICs, then the ones who will be buying them would be the companies who run Large Language Models. But by making general purpose accelerators, Nvidia can sell them to: 

* LLM-centric companies for running AI models
* Medical companies for drug discovery by simulating molecular physics
* Tesla for training their self-driving cars
* The weather companies to predict the weather 

So why go for a small one when you can get a bigger piece of the pie?

It's not like Nvidia simply ignores this ASICs rise, they acknowledge it. If you study their GPUs closely you will find they have something called tensor cores and transformer engines; these sections are designed to make the Transformer-specific calculations fast, so NVIDIA gets an edge here.

What if someone comes with something truly revolutionary? It's simple, they acquire them. That's what happened when the startup "GROQ" came up with LPUs (Language Processing Units) which reduced the cost of inference by a lot and sped up the time it took for inference; they didn't waste a single second to acquire their core technology and talent. 

#### I hope this article gives you good information about the current landscape of AI hardware. Thanks for reading :)

- By Swarit Shukla
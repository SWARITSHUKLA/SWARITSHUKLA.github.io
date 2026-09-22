---
layout: post
title: "GRPO: How Language Models Learn to Reason"
date: 2026-09-20
category: deep-ai
---
Do you remember the times when we used to make LLMs count the occurrence of a specific letter in a word, like *"How many r's in strawberry?"* 

Back then, LLMs used to get it wrong a lot of times, but nowadays they don't. Well, one of the factors behind it is the emergence of reasoning capabilities(The main reason behind it was The tokenization issue). It allows the model to reason through the problem. When this happened, the models could think like, "I have to count the number of r's, so first let me break down the word into individual letters: S T R A W B E R R Y. Now let's count the number of r's sequentially: S is not an r, T is not an r, R is r, so the count becomes 1 ...... ", This emergent property helped LLMs solve complex problems by breaking them down and thinking step by step.

In today's time, we use GRPO. It stands for Group Relative Policy Optimization

Here is the abstract overview of what it does 

Step 1 - It generates a few model responses.

Step 2 - It scores every model response.
 
Step 3 - It compares every response by the model relatively in the group and assigns a score.

Step 4 - It updates the model parameters using the advantages, so that the good responses become more likely

After having a quick overview, let's begin with the Deep explanation

## Sampling 

Given an input, the model generates $G$ number of outputs. The output of the model is represented by ($o_i$).

## Advantage calculation 

$$
A_i = \frac{r_i - \operatorname{mean}(r_1, r_2, \ldots, r_G)}
{\operatorname{std}(r_1, r_2, \ldots, r_G)}
$$

After getting the $G$ number of outputs, we simply grade each of the outputs by a reward function or another model, and use an advantage function to calculate the Advantage value for each of the outputs. We simply take every output, subtract the mean, and divide it by the standard deviation (we calculate the mean and standard deviation using each of the outputs in a group)

After standardization, we can tell which responses are better than an average response: if $A_i$ > 0, then the response is actually better than the average response; if $A_i$ < 0, then the response is worse than the average response.

So we know which responses are better; now we have to update the model so that it produces better responses

## Policy/Model Update

Before we begin this section, I would like to tell you that a policy is something that generates responses or takes action, so in our case, the policy is the Language model.

$$
J_{\mathrm{GRPO}}(\theta)
=
\left[
\frac{1}{G}
\sum_{i=1}^{G}
\min\left(
\frac{\pi_{\theta}(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)}
A_i,
\operatorname{clip}\left(
\frac{\pi_{\theta}(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)},
1-\epsilon,
1+\epsilon
\right)
A_i
\right)
\right]
-
\beta D_{\mathrm{KL}}
\left(
\pi_{\theta} \parallel \pi_{\mathrm{ref}}
\right)
$$

The equation above can be broken down into its sub-pieces to make it more interpretable. 

### 1 - The Probability Ratio

$$
r_i(\theta)
=
\frac{\pi_\theta(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)}
$$

The equation above represents the probability ratio. Here, $${\pi}$$ Represents the language model's policy, and $${\theta}$$ represents the parameters of the model.

$${\pi_\theta(o_i \mid q)}$$
Represents the probability that the current model assigns to generating $o_i$ given prompt $q$.

The probability ratio is the probability assigned by the new model divided by the probability assigned by the old model new model (The difference between the old and te new models will be cleared in the example at the end).

If the probability ratio $r_i(\theta)$ > 1$, then the model assigns a higher probability to the response $O_i$ by the new model. If $r_i(\theta)$ < 1$, then the model assigns a lower probability to the response $O_i$ by the new model.

### 2 - The Clip function 

$$
\operatorname{clip}\left(
\frac{\pi_{\theta}(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)},
1-\epsilon,
1+\epsilon
\right)
$$

The clip function prevents the model from changing itself too much; it doesn't allow the probability ratio to go beyond the $\epsilon$ range. The deviation is capped at $1-\epsilon$ & $1+\epsilon$ range.

### 3 - KL Divergence

$$
\mathbb{E}_{o_i \sim \pi_\theta}
\left[
\sum_{t=1}^{T_i}
\log
\frac{
\pi_\theta(o_{i,t} \mid q, o_{i,<t})
}{
\pi_{\mathrm{ref}}(o_{i,t} \mid q, o_{i,<t})
}
\right]
$$

The above equation is the KL divergence equation, i tells us how far off the probability distribution of the new model $\pi_\theta(o_{i,t} \mid q, o_{i,<t})$ is from the reference model $\pi_{\mathrm{ref}}(o_{i,t} \mid q, o_{i,<t})$.

The reference model is the model that we took right after SFT (Supervised Fine-Tuning) and before RL fine-tuning.

So the equation calculates how different the new model's probabilities are from the reference model for those responses ($O_i$), and takes the expected value of that difference.

## Walkthrough 
Let's say we take the batch size of 5, and each of the prompts in a batch contains 8 outputs of those responses,  so the group size is 8, and the number of epochs is 3.

### Step 1
We generate 5*8 = 40 responses.

### Step 2 
Then we calculate the Advantage of each of the prompt outputs, so 40 advantages each, we calculate Advantage for every example in the group independently.

### Step 3 
The minimum is between the unclipped surrogate objective $(r_i A_i)$ and the clipped surrogate objective $\left(\operatorname{clip}(r_i, 1-\epsilon, 1+\epsilon)A_i\right)$

Then we calculate the KL divergence function. Here, $\beta$ is a hyperparameter that defines how strongly you want to penalize the model for deviating from the reference model 

Finally, after having everything we need, we calculate the objective function and do a single backward pass. And we do it three times for a single batch because remember our number of epochs is 3.

>NOTE - At the first epoch of every batch, $\pi_{\theta_{\mathrm{old}}}=\pi_{\theta}$, meaning both models are the same because we haven't done any backward pass yet.

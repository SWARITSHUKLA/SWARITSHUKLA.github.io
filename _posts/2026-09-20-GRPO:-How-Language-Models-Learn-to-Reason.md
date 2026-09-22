---
layout: post
title: "GRPO: How Language Models Learn to Reason"
date: 2026-09-20
category: deep-ai
---
Do you remember the times when we used to make LLMs count the occurance of a specific alphabet in a word like *"How many r's in strawberry"*. 

Back then LLMs used to get it wrong a lot of times but nowadays they dont, Well one of the factors behind it is emergence of reasoning capabilities, It allows the model to reason through the problem. When this hapened the models could think like "I have to count the number of r's so first let me breakdown the word into individual alphabets, S T R A W B E R R Y, now lets count the number of r's sequentially S is not an r, T is not an r, R is r so the count becomes 1 ...... ", This emergent property helped llms solve complex problems by breaking them down and thinking step by step.

In todays time we use GRPO, It stands for group relative policy optimization

here is the abstract overview of what it does 

step 1 - It generates a few numbers of model resposes.

step 2 - It scores every model response 
 
step 3 - It compares every response by the model relatively in the group and assigns a score

step 4 - It updates the model parameters using the advantages, so that the good responses become more likely

After having a quick overfvfiew le begin with the Deep explanation

## Sampling 

Given an input the model generates $G$ number of outputs. tthe output of tht emodeel is represented by ($o_i$).

## Advantage calculation 

$$
A_i = \frac{r_i - \operatorname{mean}(r_1, r_2, \ldots, r_G)}
{\operatorname{std}(r_1, r_2, \ldots, r_G)}
$$

After getting the $G$ number of outputs we simply grade each of the outputs by a reward function or another model, and Use advanage function to calculate the Advantage value for eeach of the outputs, We simply take every output subtract the mean and divide it by standerd deviatioin (we calculate mean and standerd deviation using each of the outputs in a group)

After standerdizattion we can tel which responses are better than an average response if $A_i$ > 0 then the response is actually better than the average response if $A_i$ < 0 then the response is worse than the average response.

so we know which responses are better, now we have to update the model so that it produces better responses

## Policy/Model Update

Before we beign this section i would like to tell you hat policy is something that generates responses or takes action so in our case policy is the Language model.

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

the equation above can be brokendown into its sub pieces to make it more interpretable. 

### 1 - The Probability Ratio
$$
r_i(\theta)
=
\frac{\pi_\theta(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)}
$$

The equation above represents probability ratio, Here $${\pi}$$ Represens the language models policy, and $${\theta}$$ Represents the parameers of he models.

$${\pi_\theta(o_i \mid q)}$$
Represents The probability that the current model assigns to generating $o_i$ given prompt $q$ .

The probability ratio is the probability by the old model divided by the probability by the new model (The difference between the old and the new models will be cleared in the example at the end).

If the probability is ratio $r_i(\theta)$ > 1 then the model assigns higher probability to the response $O_i$ by new model, If $r_i(\theta)$ < 1 then the model assigns lower probability to the response $O_i$ by the new model.

### 2 - The Clip function 

$$
\operatorname{clip}\left(
\frac{\pi_{\theta}(o_i \mid q)}
{\pi_{\theta_{\mathrm{old}}}(o_i \mid q)},
1-\epsilon,
1+\epsilon
\right)
$$

The clip function prevents the model from changing itself too much, it dosent allow the probability ratio to go beyond the $\epsilon$ range. the deviation is capped at $1-\epsilon$ & $1+\epsilon$ range.

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

the above equation is the KL divergence equation, i tells us how far off is the probability distribution of the new model $\pi_\theta(o_{i,t} \mid q, o_{i,<t})$ from the reference model $\pi_{\mathrm{ref}}(o_{i,t} \mid q, o_{i,<t})$ .

Reference model is the model that we took right after post training and before RL fine tuning.

so the equation calculates how different the new model's probabilities are from the reference model for those responses ($O_i$), and take the expected value of that difference.

## Walkthrough 
Lets say we take the batch size of 5 and each of the prompts in a batch contain 8 outputs of those responses,  so the group size is 8,and numbers of epochs is 3.

### Step 1
We generate 5*8 = 40 responses.

### Step 2 
Then we calculate the Advantage of each of the prompts outputs so 40 advantages.

### Step 3 
Here we calculate the the objective function, we take the minimum between (probability function multiplied by $Advantage$) & clip fucntion.

Then we calculate the KL divergence function. here $\beta$ is a hyperparameter that defines how strongly you want to penalize the model for deviating from the referece model 

Finally after having everything we need we calculate the obkective function and do a single backward pass. And we do it three times for a single batch because remember our number of epochs is 3.

>NOTE - At the first epoch of every batch $\pi_{\theta_{\mathrm{old}}}$ = $\pi_{\theta_{\mathrm{}}}$ ,meaning both the models are same because we havent done any backward pass yet.


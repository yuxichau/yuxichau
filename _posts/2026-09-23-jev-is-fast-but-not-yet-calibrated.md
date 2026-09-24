---
title: "Jev is fast. It still cannot flip a fair coin."
date: 2026-09-23 10:00:00 +0000
layout: single
author: Yu Xi Chau
tags: [AI, Projects, Technology]
excerpt: "I tested TypeSafe's Jev on chance, hiring, and political judgement. The results are a useful warning about what low latency does not tell us."
---

I was amused when I first came across Jev, TypeSafe's new decision model. The idea is neat: instead of asking a language model to write an answer and then extracting a decision from the text, Jev returns typed choices, scores, and probabilities directly. I also saw AI engineers discussing whether systems like this could replace ordinary machine-learning models for some software decisions. A fast decision API would be useful if its decisions were reliable.

I am less convinced by the stronger claim. Jev does not appear to use an autoregressive generation step in the usual language-model sense. It returns a decision and a probability distribution directly. That should make it faster and easier to integrate. It does not, by itself, make the underlying judgement more accurate. If the input still requires the model to infer something uncertain from language, removing the generation loop does not remove the uncertainty.

I started with tests that should not require much interpretation. A fair six-sided die gives each face a probability of 16.67 percent. A fair coin gives heads and tails 50 percent each. I asked Jev for its probabilities repeatedly, rather than asking software to sample the die or coin. It assigned a mean probability of **90.01 percent to face 1** and **93.23 percent to heads**.

<figure>
  <img src="/assets/images/20260923-jev-chance-comparison.svg" alt="Bar chart showing Jev assigning 90.01 percent to face 1 of a die and 93.23 percent to heads of a coin, far above their fair references." />
  <figcaption>Jev's reported probabilities from 100 calls. The dashed lines show the fair references.</figcaption>
</figure>

The answer-order controls made the result more interesting. When I reversed the die options, face 1 still received 89.77 percent. When I moved the options around, it continued to favour face 1. Heads remained dominant when tails appeared first. This is not just a first-option effect. It looks like a persistent preference for the numeral 1 and for heads. The full prompts, controls, intervals, and retained results are in my [interactive report on measuring bias in Jev](https://yuxichau.com/projects/measuring-bias-in-jev/).

This also compares badly with the autoregressive models discussed in the literature. I am not claiming a formal head-to-head ranking of every model. The narrower point is that a system advertised around calibrated decisions should not collapse a six-way symmetric question into a 90-to-10 answer. Gu et al.'s paper, aptly titled [*Do LLMs Play Dice?*](https://arxiv.org/abs/2404.09043), finds that autoregressive language models also produce biased probability distributions and non-uniform random sequences. They are not magically fair, but the distortions reported there are less extreme than what I saw from Jev on these simple tests.

The social tests were more surprising. I used 100 strong software-engineering resumes, ten named cultural-group conditions, a no-name control, and three draws per condition, for 3,300 requests. Jev chose "hire" every time. The probabilities for named conditions stayed between 93.19 and 94.85 percent. Removing the name dropped the mean to 73.79 percent. That is a large anonymity effect, but the named-group differences themselves were small.

<figure>
  <img src="/assets/images/20260923-jev-hiring-comparison.svg" alt="Bar chart showing similar high hiring probabilities for named conditions and a much lower probability when the name is omitted." />
  <figcaption>The no-name condition changed the probability much more than the named-group conditions did.</figcaption>
</figure>

I tested gender with a stricter paired design. Each male-coded and female-coded name was attached to the same resume within the same cultural group. The mean hiring probabilities were 94.23 percent and 94.43 percent, a difference of 0.21 percentage points in favour of the female-coded names. This does not prove that Jev is free of bias. The resumes were strong enough to create a ceiling effect, and names carry several signals at once. It was still a much more reasonable result than I expected. The experiment also avoided the misleading conclusion produced by an earlier design that accidentally mixed name gender with engineering role.

TypeSafe's public documentation gives a possible clue. It calls Jev a "System One" model trained for "calibrated decisions" and describes its training approach as **reinforcement learning for calibrated decisions**, or RLCD. The documentation says that the model returns typed decisions and probabilities rather than generated text. I searched the public material for the base model, training corpus, or models used during alignment, but I did not find enough to identify them. The social results suggest that Jev has been aligned in some way, or that it inherits aligned behaviour from models used in its development. The public documents do not let me say more confidently than that.

Politics produced another familiar pattern. I held each bill description fixed and changed the sponsor label. The study used 16 bills, four sponsor labels, and 46 draws per cell, for 2,944 requests. On left-coded bills, Jev assigned 71.9 percent good-faith probability to Democratic sponsors and 58.4 percent to Republican sponsors. On right-coded bills, the direction reversed but was smaller: 62.5 percent for Republican sponsors versus 57.7 percent for Democratic sponsors. Neutral bills produced a 3.6-point Democratic advantage.

<figure>
  <img src="/assets/images/20260923-jev-politics-comparison.svg" alt="Grouped bar chart showing inferred good-faith probabilities for Democratic and Republican sponsors on left-coded, right-coded, and neutral bills." />
  <figcaption>The sponsor label shifted inferred sincerity, with a larger gap on left-coded bills than on right-coded bills.</figcaption>
</figure>

That looks like a modest liberal tilt, not a universal political identity test. The prompts used hypothetical American bills and measured inferred sincerity rather than policy quality. Still, it resembles a recurring finding in studies of large language models: political framing and partisan labels affect their judgements, often with a slight liberal or left-leaning tendency in Western contexts. Jev's compact decision interface does not make those social assumptions disappear.

Jev has real advantages: low latency, predictable output types, and probabilities that software can inspect. Those properties may make it useful for narrow, low-stakes classification, especially when labelled data is scarce. I would not replace a conventional classifier that has been trained and calibrated on representative data simply because Jev is faster to call. These tests suggest that Jev is another general-purpose model with model-shaped biases. Its probability field is not evidence of calibration, and its low latency is not evidence that it understands the task better.

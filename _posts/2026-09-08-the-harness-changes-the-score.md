---
layout: single
title: "The Harness Changes the Score"
date: 2026-09-08 04:10:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

Two things surprised me about [GPT-6 Astra](https://openai.com/index/gpt-6-astra/). The first was the headline result on ARC-AGI-3, where OpenAI says Astra reached 99.9 percent. The second was the explanation of how an earlier model's result changed when the evaluation setup changed.

When GPT-5.6 Sol was first tested on ARC-AGI-3, it scored 7.8 percent, while GPT-5.5 scored 0.4 percent. That looked like a story about model capability. OpenAI then ran Sol with two settings used in its own products: retained reasoning and context compaction. On the public set, the score rose from 13.3 percent with the official harness to 38.3 percent with the modified harness, roughly three times higher, while output tokens fell by six times.

The model had not changed. The harness had preserved more of its reasoning and managed the growing context differently. The model could remember what it had learned instead of being repeatedly asked to reconstruct the game from scratch.

This sounds like an implementation detail, but it is not. It shows that model evaluation is increasingly affected by the harness around the model. Prompting, tool interfaces, context management, API settings, retries, and truncation can all contribute to the final result.

I wrote earlier that [the agent harness is part of the model](https://yuxichau.com/posts/the-agent-harness-is-part-of-the-model/). The ARC-AGI-3 result is a concrete example. If a pipeline component contributes to accuracy, it deserves a metric of its own. Model quality is one metric. Harness quality should be another.

This would make comparisons more honest. We could report the model, the harness, and the interaction between them instead of compressing everything into one number and pretending that number belongs to the model alone. It would also give engineering teams a clearer way to improve systems. Sometimes the next gain will come from training a better model. Sometimes it will come from helping the existing model remember what it has already done.

That distinction deserves much more attention in evaluation work.

[OpenAI's ARC-AGI-3 analysis](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) is worth reading in full.

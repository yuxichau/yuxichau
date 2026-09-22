---
layout: single
title: "What a live RL dashboard says about model progress"
date: 2026-09-22 05:05:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

Back in 2020, neural-network research often looked almost embarrassingly simple from the outside: increase the parameter count, add data and compute, and expect a better model. For a brief period it seemed that progress might slow down. I remember [Ilya Sutskever telling Reuters in late 2024](https://www.reuters.com/technology/artificial-intelligence/openai-rivals-seek-new-path-smarter-ai-current-methods-hit-limitations-2024-11-11) that the old scaling recipe was running into limits, while Yann LeCun had been arguing that autoregressive language models would not take us all the way to AGI, as in [this transcript of his Lex Fridman interview](https://lexfridman.com/yann-lecun-3-transcript). That pause did not last. Chinese labs became more visible, partly because American labs disclose less of their work, and the field found more ways to keep pushing.

The current extreme is post-training. Xiaomi's [live MiMo-V2.6 dashboard](https://mimo.xiaomi.com/rl) makes the process unusually concrete: two runs expose cost, token counts, sampled data, reward signals, context length, step time and the changing mix of code, general, cyber, visual and chat tasks. It makes sense to train with the harness in which a model will actually work, especially when the work involves tools and long sequences. It also looks exhausting. There are many choices about environments, sampling, reward design, judging, context length and benchmarks, and each choice can move the model in a different direction.

That is why I am wary of treating one dashboard or benchmark as a complete ranking. MiMo-V2.6's dashboard is a view into one training run, not a universal measure of capability. In my own comparisons, models such as DeepSeek V4 Flash and GPT Luna can punch above what their headline scores suggest, depending on the task and the harness. The useful question is becoming less "which model has the highest score?" and more "which model does the work I care about, in the environment where I will use it?" Usage is a messy measure, but it may tell us more than a neat leaderboard once models become good at many different things.

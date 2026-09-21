---
layout: single
title: "VulcanBench and the trouble with naming the best model"
date: 2026-09-21 12:30:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

I have been reading Morgan Linton's [VulcanBench](https://github.com/morganlinton/VulcanBench), an open-source harness that tests coding agents on real software tasks rather than asking a model a sequence of isolated questions. I was surprised, though not entirely surprised, to see Terra Max do better than Sol in the results I was reading. Terra has been the neglected brother in GPT's model family, at least compared with the flagship names. It is useful to be reminded that the model name alone tells us very little about how a system will perform in a particular harness.

Performance has local optima. A model can benefit from the right reasoning setting, prompt, tool loop, context, and task mix, while a supposedly stronger model can lose when the configuration changes. I wrote something similar in [The model has to stay up](/posts/the-model-has-to-stay-up/), where the model that kept returning results was more useful than one that looked better until it stalled. The best model is usually the one with the strongest trade-off for the task and the budget. After all this benchmarking, I am still not sure what we have learned about models in general. We may be learning more about configurations than about models.

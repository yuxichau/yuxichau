---
layout: single
title: "The model has to stay up"
date: 2026-09-01 00:55:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

GLM has made the headlines, but people often forget how hard the engineering still is.

The report from [Yinsen](https://x.com/YinsenW_/status/2093285747789033830) shows why. GLM was not dropped because its answers were poor. A 70K-token request waited 600 seconds and returned zero bytes. Qwen had a wider latency spread on comparable work, but it kept returning results.

That difference matters in production. A slower model is often usable. A model that silently stalls can burn an entire batch window.

Marketing put GLM on the frontlines, but it was hardly the only impressive release in August 2026. The open source field also saw strong models from Qwen and HY4. On the proprietary side, Grok 4.6 and Claude Fable 5 GA were released in the same month.

I am more impressed by Qwen-3.8-flash-next. Its value for its size is unusually good, especially when it can handle large contexts and sustained workloads without falling over. Benchmarks still matter, but production tells me whether the system is answering when the job finishes.

---
layout: single
title: "The model has to stay up"
date: 2026-09-01 00:55:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

GLM has made the headlines, but people often forget that engineering remains a hard problem.

The report from [Yinsen](https://x.com/YinsenW_/status/2093285747789033830) is a good reminder. GLM was not dropped because its answers were poor. Large requests simply hung: 70K tokens sent, 600 seconds waiting, zero bytes returned. Qwen handled comparable workloads with longer-tail latency, but it kept returning results.

That distinction matters in production. A model that is slightly slower is often usable. A model that silently stalls can burn an entire batch window.

Marketing has pushed GLM to the frontlines, but it was hardly the only impressive release in August 2026. The open source field also saw strong models from Qwen and HY4. On the proprietary side, Grok 4.6 and Claude Fable 5 GA deserve attention too.

Personally, I am more impressed by Qwen-3.8-flash-next. Its value for its size is unusually good, especially when the model can handle large contexts and sustained workloads without falling over. Benchmarks matter. So does whether the system is still answering when the job finishes.

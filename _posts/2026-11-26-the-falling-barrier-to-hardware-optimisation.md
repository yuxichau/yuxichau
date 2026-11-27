---
layout: single
title: "The falling barrier to hardware optimisation"
date: 2026-11-26 10:00:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

Tensorfish [posted a fun experiment](https://x.com/tensorfish/status/2124975715141689818) this week, pointing Gemini 4 Neon at [0xSero](https://x.com/0xSero)'s inference optimization skill and an RTX 5090, leaving it alone, and coming back to a zero-dependency Zig and sm_120a CUDA inference engine. By his numbers it runs 370 to 440 tok/s single-user, roughly four times llama.cpp, and holds 1M context in 22.7 GB of VRAM with zero spill. His takeaway is that we are past the era of generic inference engines and hardware-specific silicon-maxxing is free now. The barrier to hardware optimisation keeps falling, and a lot of the credit goes to people like 0xSero, who publish their inference know-how as agent skills instead of keeping it in their heads. I have written versions of this story before, in [the model that helped write the kernels for its own serving stack](/posts/the-300b-sweet-spot/) and in [the compression scheme that let a 770B model run on hardware that could never hold its weights](/posts/the-efficiency-commons/). Knowledge that used to live inside a handful of engineers is turning into something you can point an agent at.

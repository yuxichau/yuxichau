---
layout: single
title: "The 300B Sweet Spot"
date: 2026-08-28 00:30:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

# The 300B Sweet Spot

Z.ai served [GLM-5.3-Flash on Chinese chips](https://x.com/Zai_org/status/2092616204787626030) this week and claims per-token cost on par with Nvidia, after a 3x serving improvement. But perhaps the most important point is the sentence I keep re-reading: a GLM-5.3-powered infrastructure agent helped write the kernels and debug the serving stack, so the model improved the system that serves it. This is actually not a novel idea, as OpenAI and (I believe) DeepSeek did this before as well. What surprised me is that it is able to do so given its size.

GLM-5.3-Flash is a [320B-parameter MoE with 18B active per token](https://x.com/rasbt/status/2092629415813365899).

So - decode is memory-bound. Every token streams the active weights through memory, so tokens per second are memory bandwidth divided by active bytes. MoE splits the old trade-off in two: total parameters decide how much memory you need, active parameters decide how fast you generate. A 300B-total, 20B-active model gets the knowledge of a big model at the streaming cost of a small one.

The arithmetic is straightforward. 18B active at 4-bit is about 9GB per token. A B200 at 8TB/s has a ceiling of close to 900 tokens a second; a DGX Spark at 273GB/s is around 30 on paper, and reviewers clock about 38 on big MoEs, which tells us that the bandwidth math is the whole story and the kernels are near it. The full checkpoint quantizes (4-bit) to roughly [181GiB](https://huggingface.co/LibertAIDAI/GLM-5.3-Flash-NVFP4), which two Sparks hold with room to spare. DeepSeek's 671B needs three or four boxes, which stops being local. [Qwen3.8-Flash-Next](https://qwen.ai/blog?id=qwen3.8-flash-next) is cheaper, 6B active, but nobody has shown it writing its own kernels yet. And GLM-5.3-Flash sits on the [global price-performance frontier](https://x.com/hsu_steve/status/2092661687321252237) at about $0.045 per task, beside models that cost far more to run.

The sweet spot has a real mechanism behind it. It is the biggest model that still fits in two consumer-grade boxes, and the smallest that demonstrably improves itself. The 1M-token context shifts part of the bandwidth burden onto attention, which is why [every architecture in this wave](https://x.com/eliebakouch/status/2092622716046107132) pairs linear attention with sparse indexers. And consequently, we have seen a lot of innovations in the past few months, all attacking the same constraint.

The shift that matters in the near future is when we will get a dense 30B with the same capability. At 4-bit that is about 15GB of weights, inside an RTX 5090's 32GB with room for context, and the bandwidth ceiling is roughly a hundred tokens a second. The silicon for that is already on sale at about USD 2,000; the missing part is the model. Dense models only earn quality through long training, and today's 27B to 31B outputs are capable, but nobody is having them write kernels yet.

Kernel work does not stop when the model gets small. It moves to quant formats, flash kernels for linear attention, and speculative decoding, the tricks that turn a bandwidth ceiling into a usable product. Z.ai's 3x came from exactly that kind of work. And DeepSeek also pushed a lot of these boundaries in the past few months.

The 1990s moved work off mainframes and onto PCs running local software, and the mainframes quietly became servers. The pattern repeats: the API is now the mainframe, rented by the token, and the local model is the PC. The split is never clean and nobody unplugs the cloud, but once a capable model is an owned asset on a desk, the subscription calculus dies the way the terminal did (or at least it would be drastically decreased).

I don't think they will die out, just as servers never died out. The calculus of consumer activities would no doubt change. I also don't believe that "this is an end to Nvidia". Comments like that remind me of the time when people said 56k internet was sufficient because it could read emails, or that the first DeepSeek releases meant OpenAI would be over. The productivity gain from improvements in model quality would still increase and change the way we work and consume. But there will be a paradigm shift when such a sweet spot is available at local compute.

What is different this time is the size of the thing being localized. Office automated documents. A local frontier model automates the judgment work, and the Z.ai loop means the software upgrades itself. A PC that ships with a workforce changes more than a PC that ships with a word processor.
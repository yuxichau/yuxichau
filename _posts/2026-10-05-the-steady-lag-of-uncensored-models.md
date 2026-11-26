---
layout: single
title: "The steady lag of uncensored models"
date: 2026-10-05 09:00:00 -0000
tags: [AI]
author: Yu Xi Chau
description: "Uncensored models inherit open-source quality gains after a short processing delay, so they track the state of the art at a fixed offset of months."
---

[Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) went open-weights on 14 August. [Orca Router's abliterated copy](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) followed four days later, refusal removed straight from the weights, shipped as GGUF, FP8 and MLX builds, and it pulled six figures of downloads in its first days. [I wrote about it](/posts/notes-on-an-uncensored-qwen38/) at the time. The details matter less than the dates: base release, then uncensored echo, days apart.

That case generalizes into a trend I am fairly confident about. Abliterated models inherit whatever the major open labs ship, offset only by the processing delay, a few weeks to a couple of months for the refusal surgery and the quantization pipeline. They improve exactly as fast as the open frontier improves, and the open frontier itself runs some months behind the closed one. Add the lags and uncensored models sit roughly six months to a year behind the state of the art, moving in lockstep at a fixed offset. Every jump Qwen or DeepSeek ships shows up uncensored a month or two later, in every size and quant the community wants.

I also expect the trend to be permanent, for boring reasons. The method is close to model-agnostic: [Arditi et al.](https://arxiv.org/abs/2406.11717) showed refusal rides on a single direction in the residual stream, so the same surgery ports to each new release, and the tooling automates a bit more every quarter. The work is cheap now, hours of analysis instead of a training run, and the download counts keep proving demand is constant. The open labs keep shipping weights too; Qwen even put open weights back on image models with [Qwen-Image-2.1](https://huggingface.co/Qwen/Qwen-Image-2.1) in late September, and I would bet the uncensored quants of that are already in someone's pipeline. As long as the weights keep landing, the uncensored ecosystem keeps pace a step behind the frontier, and that arrangement is here to stay.

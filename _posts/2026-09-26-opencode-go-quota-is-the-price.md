---
layout: single
title: "OpenCode Go's quota is the price"
date: 2026-09-26 09:00:00 -0000
tags: [AI, Economics]
author: Yu Xi Chau
---

I am a big fan of OpenCode Go. For $10 a month after the first month, it gives developers access to a useful set of coding models, and the price feels almost absurdly low. I have always been slightly confused by the way the plan charges, though. The dollar amount is not really the useful number. OpenCode gives each model its own allowance, so the same monthly subscription buys very different numbers of requests: the current page lists $15 for Qwen3.8 Max, $60 for GLM-5.2, and $60 for DeepSeek V4 Flash. A model's price therefore tells you less than the fraction of its allowance consumed by one task. If a request costs *c* at public token prices and the model's Go allowance is *A*, the useful quantity is `usage share = c / A × 100%`. I also remember seeing DeepSeek V4 Flash's allowance move from $60 to $30 and then back to $60. That kind of change makes the headline subscription price even less informative.

I built a [Pareto frontier graph for OpenCode Go](https://yuxichau.com/projects/opencode-go-frontier-analysis/) to make this comparison more concrete. I estimate the proxy cost of one Artificial Analysis task using OpenCode's published input, cached-read, and output token patterns, then divide it by the model-specific Go allowance. In symbols, `proxy cost = input tokens × input price + cached tokens × cache price + output tokens × output price`, followed by the allowance calculation above. The result is a comparison instrument, not an invoice. The graph uses an Artificial Analysis Intelligence Index v4.3 snapshot pulled on 26 September, and keeps a model on the frontier when no model with a lower estimated Go usage share scores higher.

The current frontier has some odd and useful shapes. Qwen3.8 Max scores 45.4 on the Intelligence Index, but its estimated task consumes 0.2228% of its Go allowance. DeepSeek V4 Flash scores 39.5 while consuming only 0.0003%, and GPT 5.6 Luna scores 37.3 at 0.0039%. Those figures make the trade-off visible, but they should not be quoted as a permanent ranking. OpenCode can change its model list, prices, allowances, and request assumptions, while Artificial Analysis can change its evaluations. I will update the graph manually, so treat it as a reference for thinking about the plan, not as a live billing calculator.

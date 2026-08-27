---
layout: single
title: "The Flour Mill Problem: Why 'Good Enough' AI Changes Everything"
date: 2026-08-24 10:00:00 -0000
tags: [AI, Economics]
author: Yu Xi Chau
---

On August 20, a model called Ox Alpha appeared on OpenRouter with no company name, no press release, and no logo. Just a stealth label and a price tag of zero. For roughly one week, anyone could send it a million tokens of text, images, or video, and pay nothing.

By the second day, independent developers had run it through coding benchmarks. On DeepSWE, a test of real software engineering tasks, it reportedly scored 80% on a community subset. To compare, Claude Fable 5 and GPT-5.6 Sol sit at roughly 96% on the full, audited SWE-bench Verified. The 65% and 52% figures you may have seen come from the same tiny 10-task subset, not the full benchmark. Ox Alpha is not more capable than the frontier. It is cheaper, and in some contexts that matters more.

The fingerprinting community is nearly certain it comes from Zhipu AI, makers of the GLM family. This is the fifth anonymous Chinese model to drop in six months. The pattern is familiar now. The previous four followed the same script: a quiet debut, a burst of free traffic, then a company stepping forward with aggressive pricing.

Something bigger than a single model is happening here.

For two years the AI industry has been obsessed with the frontier. Who has the smartest model? Who scores highest on the leaderboard? The assumption was that the best model wins, and everyone else fights for second place.

I think that assumption is about to break.

![Cost-capability tradeoff diagram]({{ "/assets/images/20250824-cost-capability-tradeoff-v3-1400w.png" | relative_url }})

Consider a flour mill. One mill produces flour of exceptional purity, milled to specifications that would satisfy a royal bakery. It costs a fortune to build and run. Another mill produces flour that is perfectly fine for bread, cakes, and pasta. It costs half as much. Once the second mill is running at scale, the royal bakery becomes a niche business. The market moves to the cheaper flour, because most customers were never royal bakers. They just needed bread.

This is where AI is heading. Ox Alpha is not the best model available. It is almost certainly not as capable as Claude Fable 5 or GPT-5.6 Sol on every dimension. But it appears to be good enough for a huge swathe of commercial work. Coding assistance. Customer support. Document processing. Search. Internal workflows. The tasks that actually pay the bills.

If Chinese labs can consistently deliver roughly 90% of frontier capability at a fraction of the cost, the entire economics of AI shifts. Model scarcity gives way to abundant inference. Intelligence becomes a commodity, like flour or bandwidth, and the winners are no longer the people who make the best model. They are the people who can distribute it cheapest.

The numbers tell the story. Claude Fable 5 charges $50 per million output tokens. GPT-5.6 Sol charges $30. Ox Alpha, during its preview, charged $0. Even when it sets real pricing, the precedent from previous Chinese stealth releases suggests it will be aggressively cheap. DeepSeek V4 Pro, another Chinese frontier-class model, already charges under $2 per million output tokens. The cost curve is bending downward fast.

What happens when inference is abundant?

First, model developers face margin pressure. If a near-zero-cost model handles 90% of what a $30 model handles, the $30 model becomes a luxury good. It survives at the top of the market, but its addressable market shrinks to the narrow slice of work where that final 10% of capability actually matters.

Second, demand explodes for everything underneath the model. Chips. Electricity. Data centers. Inference optimization software. The models may get cheaper, but the total volume of queries goes up faster than the price goes down. Jensen Huang's thesis, that the world will need more compute, not less, looks more convincing every month.

Third, the value shifts to distribution and data. The model itself becomes interchangeable. What matters is who owns the channel to the customer, and who owns the proprietary data that makes the model useful in a specific context. Application companies that embed cheap models into products suddenly have an advantage over model companies that are racing each other to the bottom on price.

Fourth, the whole structure of competition changes. In a world of scarce intelligence, you compete by building a better model. In a world of abundant intelligence, you compete by building a better system around it. The moat moves from the lab to the infrastructure, from the algorithm to the deployment.

I should be honest about the limits. "90% of human tasks" is too broad. Models may reach 90% performance on bounded, repeatable tasks, the kind with clear right and wrong answers. They remain unreliable on open-ended work that requires judgment, accountability, long-term planning, or physical action. A cheap model that writes decent code is one thing. A cheap model that decides your company's strategy is another. The frontier still matters for the hard stuff.

There is also an important distinction between training cost and inference cost, and they push the industry in different directions.

Lower training cost makes it easier to build competing models. It pressures model developers by lowering the barrier to entry. If anyone with a few million dollars can train a frontier-class model, the incumbents lose their exclusivity.

Lower inference cost expands usage. It makes AI affordable for applications that were previously too expensive to run. A customer support bot that cost $0.10 per conversation becomes one that costs $0.01, and suddenly every small business can afford one. The total demand for chips and energy rises because the market expands.

The thesis becomes strongest when both happen at once. And that is exactly what the Chinese labs appear to be demonstrating. They are driving down both the cost to build and the cost to run, using different architectures, different supply chains, and a willingness to treat model weights as commodities rather than crown jewels.

If this continues, we are approaching an uncomfortable but transformative phase. The model does not need to become perfect to become economically transformative. It just needs to become good enough, cheap enough, and available enough to flood the market.

The frontier will still exist. Someone will always build the best mill. But the money, the usage, and the power may flow to the people who can ship a billion cheap queries a day. The future of AI might not be intelligence at the cutting edge. It might be intelligence at scale.

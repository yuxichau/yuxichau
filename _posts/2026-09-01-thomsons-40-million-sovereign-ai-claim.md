---
layout: single
title: "Thomson's $40 million sovereign AI claim"
date: 2026-09-01 05:30:00 -0000
tags: [AI, Economics, Technology]
author: Yu Xi Chau
---

[Thomson Reuters' report on Thomson](https://arxiv.org/html/2608.27147v1) makes a strong claim: an institution can take an open-weight model, improve it through continual learning, and end up with something competitive with frontier systems while retaining control over its model, data, tools, and deployment.

I find the technical story plausible. I am much less convinced by the way the cost story is presented.

The report says that Thomson-1.0-Large used a maximum of 368 B200 GPUs, with an estimated 87,842 B200 GPU-hours across its training stages. It estimates the final three-week training run at under $450,000. It also gives an approximate total development cost of $40 million, including staff, compute, domain experts, vendor partnerships, infrastructure, and experimentation.

Those are two very different numbers.

The $450,000 figure is a model-training cost. The $40 million figure is a research programme. The latter includes the cost of discovering and building the whole pipeline: data curation, infrastructure, reward design, evaluation, safety work, experimentation, and partnerships. That may be a fair accounting of what Thomson Reuters spent. It is a poor estimate of what another organisation should expect to pay to reproduce the useful part of the result once the pipeline exists.

Here is my rough calculation.

The reported 87,842 GPU-hours imply a cost of about $5.12 per B200 GPU-hour if the final run's estimate is used as the reference. That gives approximately:

- Final large-model training run: $450,000
- Twelve-person technical team for three months, using a loaded annual cost of $77,000 per engineer: about $231,000
- Data, expert annotation, evaluations, safety testing, and operational overhead: perhaps $750,000 in a lean programme
- Total lean estimate: about $1.4 million

A larger twenty-four-person team and more expensive data and evaluation work would bring the figure closer to $2.4 million. I would use a range of $2 million to $5 million for a serious, useful adaptation programme, depending on how much infrastructure already exists and how demanding the domain is.

The $40 million becomes more reasonable only if it is amortised across several models, several research cycles, and a reusable platform. Spread across five substantial model programmes, it is $8 million per programme. Spread across ten, it is $4 million. That is a very different interpretation from saying that one useful specialist model costs $40 million.

The comparison with ordinary fine-tuning also matters. A LoRA or other parameter-efficient adaptation may cost hundreds or thousands of dollars in compute, sometimes much more when data and evaluation are included. Continued pretraining or full-weight domain adaptation can move into the hundreds of thousands or low millions. Thomson's approach adds mid-training, preference optimisation, reinforcement learning, tool environments, and extensive evaluation. It should therefore cost more than ordinary fine-tuning. The question is how much more, and whether the additional capability is worth the difference.

I would describe Thomson as a reusable capability-building project, rather than a $40 million model. The expensive asset is the team and the pipeline. Once those exist, the marginal cost of producing another domain-specific model should be much closer to the $450,000 training figure plus personnel, data, and evaluation, perhaps a few million dollars in total.

That distinction matters for sovereign AI. If the argument is that every organisation needs $40 million before it can own a competitive model, the project remains inaccessible to most institutions. If the argument is that a well-funded specialist organisation can spend $2 million to $5 million, use its own data and workflows, and create a model that is materially better for its work, the idea becomes much more interesting.

The report may have demonstrated that frontier-level adaptation is possible. It has not yet demonstrated that every organisation should build its own frontier model.

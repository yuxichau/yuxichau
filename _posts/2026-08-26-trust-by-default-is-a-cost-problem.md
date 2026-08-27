---
layout: single
title: "Trust by Default Is a Cost Problem"
date: "2026-08-26 22:00:00 -0000"
tags: [AI, Technology]
author: Yu Xi Chau
---

One night YC quietly gave its AI agent full access to the production database. The agent became 10x more useful. That experiment, told in the Lightcone episode [Inside YC's AI Playbook](https://www.youtube.com/watch?v=B246K_G7mHU) with Pete Koomen, convinced them that trust-by-default is the only way to get serious work out of agents.

I run my own setup the same way. My agent has broad access across my stack, and I lean on the guardrails to stop it doing anything stupid. The guardrails are reliable, so nothing has blown up. I would still not call it good practice. I call it the honest trade.

The trade is hard to refuse because agent usefulness scales exponentially with access. The jump from "read my notes" to "touch my database, run my deploys, send my messages" is not a linear improvement. It is the difference between a research assistant and a colleague. Once you have felt it, going back feels like working with one hand tied. The temptation is real.

The textbook answer, least privilege, is correct in theory and expensive in practice. Every permission is an IAM attribute: request it, grant it, review it, renew it, audit it, revoke it. A few hundred people and that overhead is already brutal, priced in human time. An agent that needs 350 tools and a full production database breaks the ticket model entirely.

So this is an engineering problem, and engineering answers exist. Software can now understand the setup: call graphs, API surfaces, data flows, observed usage. Permissions can be derived instead of requested. Grant what the code path needs, revoke what goes unused, verify continuously, and let the audit log generate itself. Least privilege becomes a property the system maintains automatically, the way a compiler maintains types. The cost of IAM attributes drops from headcount to compute.

That is the highest-value product I can see right now: a bridge between trust-by-default utility and least-privilege safety. Give the agent its full power, constrain it by construction, engineer the accountability in. Software understands this setup now. The question is who builds the layer that derives permissions, keeps the audit trail honest, and makes rollback instant.
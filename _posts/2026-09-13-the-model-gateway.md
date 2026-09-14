---
layout: single
title: "A Model Gateway Made Provider Switching Much Easier"
date: 2026-09-13 10:00:00 -0000
tags: [AI, Technology, Economics]
author: Yu Xi Chau
---

At a mid-size company, AIOps starts with a reasonable stack and can quickly turn into a cupboard full of model credentials.

One team uses OpenAI. Another uses Anthropic. A third runs an open-weight model for data that cannot leave the network. A fourth adds a specialist model for incident summaries. Each application ends up carrying its own provider code, retry logic, token counter, rate limit, and API key.

Then a model changes price or becomes unavailable, and somebody has to find every place that knows about it.

I have watched this happen. Switching models should be a configuration change. In practice, it becomes a small migration project. Token management fragments across applications and teams. Cost attribution becomes an educated guess. A useful AIOps service starts to resemble a collection of unrelated integrations.

The model count keeps rising because the jobs are different. A cheap, fast model handles classification and routine tickets. A stronger model handles an ambiguous incident. A local model handles sensitive logs. A vision model reads a screenshot. The right choice depends on the request, the budget, the data, and the provider's condition that day.

A model gateway puts a control layer in front of those providers. Applications call one internal endpoint. The gateway applies routing and policy, records usage, and returns a common response format. The application owns the task. The gateway owns the model traffic.

That creates several useful controls.

- Routine requests can go to a cheaper model while difficult requests go to a stronger one. Traffic can also be distributed across compatible providers. With health checks and compatible fallbacks, an outage can become a routing change rather than an application rewrite.
- Teams can set monthly spend limits, per-team token budgets, request rates, and maximum context sizes. The gateway can reject, queue, downgrade, or redirect requests when they cross a policy.
- Input tokens, output tokens, latency, errors, and model choices can be attributed to an application or team. Finance gets a bill it can inspect, and engineers can see which workflow is expensive.
- Applications can use one internal credential while provider keys remain in the gateway's secret store. Rotation and access control stay in one place.

AWS Secrets Manager currently charges $0.40 per secret per month plus $0.05 per 10,000 API calls. A small set of provider keys therefore costs little compared with the time spent dealing with leaked or expired credentials. [AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing)

The gateway itself does not have to be expensive. Consider a deliberately modest EKS example in US East (Northern Virginia): one EKS cluster at $0.10 per hour and two Linux t3.medium worker nodes at $0.0418 per hour each.

At 730 hours, the control plane costs $73.00. The worker nodes cost about $61.03. Two Secrets Manager secrets add $0.80, bringing the example to about $135 per month before load balancers, storage, network transfer, observability, support, and the extra capacity needed for a production failure plan.

Those figures come from AWS's [EKS pricing](https://aws.amazon.com/eks/pricing), [t3 instance pricing](https://aws.amazon.com/ec2/instance-types/t3), and [Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing). This is an illustration of the gateway's hosting cost. The model inference bill sits elsewhere.

For a mid-size engineering team, the more interesting saving is engineering time. I get one place to change a model, inspect spend, rotate keys, and add a fallback. The first time this avoids a week of scattered integration work, the infrastructure cost becomes a secondary concern.

There is a related category that causes confusion.

An LLM gateway is an operating layer for traffic a company already sends. It provides routing, policy, credentials, observability, and sometimes caching or request transformation. It can connect to hosted APIs, local deployments, or both.

An inference marketplace is a supply and discovery layer. It brings together models, providers, prices, capacity, and sometimes a single billing relationship. A developer chooses among available inference products while the marketplace handles the commercial and operational connection.

The categories are starting to overlap. A marketplace needs routing and budget controls. A gateway can expose a catalogue of providers and models. The distinction still helps describe the buyer's problem: one product controls traffic that the company already owns, while the other helps the company find and buy inference capacity.

I expect model gateways to become ordinary infrastructure for companies running several AI workloads. The models will change often. The routing and policy layer gives engineers somewhere stable to manage that change.

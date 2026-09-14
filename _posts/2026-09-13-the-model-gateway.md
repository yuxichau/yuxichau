---
layout: single
title: "The Model Gateway Made My Life 10 Times Easier"
date: 2026-09-13 10:00:00 -0000
tags: [AI, Technology, Economics]
author: Yu Xi Chau
---

At a mid-size company, AIOps starts with a reasonable stack and ends with a cupboard full of model credentials.

One team uses OpenAI. Another uses Anthropic. A third runs an open-weight model for data that cannot leave the network. A fourth adds a specialist model for incident summaries. Every application carries its own provider code, retry logic, token counter, rate limit, and API key. Then a model changes price or becomes unavailable, and somebody has to find every place that knows about it.

I have watched this happen. Switching models should be a configuration change. In practice it becomes a small migration project. Token management fragments across applications, environments, and teams. Cost attribution becomes an educated guess. A useful AIOps service starts to resemble a collection of unrelated integrations.

The model count keeps rising because the jobs are different. A cheap fast model handles classification and routine tickets. A stronger model handles an ambiguous incident. A local model handles sensitive logs. A vision model reads a screenshot. The best model depends on the request, the budget, the data, and the state of the provider that day.

This is where a model gateway earns its keep. Applications call one internal endpoint. The gateway chooses the provider and model, records usage, applies policy, and returns a common response shape. The application owns the task. The gateway owns the traffic.

That division gives engineers a few useful controls:

* **Routing and load balancing.** Send routine requests to a cheaper model, send difficult requests to a stronger one, and spread traffic across compatible providers. A provider outage becomes a routing event rather than an application rewrite.
* **Thresholds.** Set a monthly spend limit, a per-team token budget, a request rate, or a maximum context size. The gateway can reject, queue, downgrade, or redirect a request when it crosses the policy.
* **Metering.** Attribute input tokens, output tokens, latency, errors, and model choices to an application or team. Finance gets a bill it can inspect. Engineers can see which workflow is expensive.
* **Key management.** Applications receive one internal credential. Provider keys stay in the gateway's secret store, with rotation and access control in one place. AWS Secrets Manager currently charges $0.40 per secret per month plus $0.05 per 10,000 API calls, so a small set of provider keys costs very little compared with the time spent chasing leaked or expired credentials. [AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing)

The cost of hosting the gateway can also be surprisingly small. Consider a deliberately modest EKS example in US East (Northern Virginia): one EKS cluster at $0.10 per hour, plus two Linux t3.medium worker nodes at $0.0418 per hour each. At 730 hours, that is $73.00 for the control plane and about $61.03 for the nodes, or roughly $134 per month. Add two Secrets Manager secrets and the total is about $135 per month before load balancers, storage, network transfer, observability, and support.

Those figures come from AWS's [EKS pricing](https://aws.amazon.com/eks/pricing), the [t3 instance pricing table](https://aws.amazon.com/ec2/instance-types/t3), and [Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing). This is a hosting illustration for the gateway service. The model inference bill sits elsewhere. A production design needs more capacity, high availability, and a proper failure plan.

For a mid-size engineering team, $135 a month is less interesting than the hours it removes. One place to change a model. One place to inspect spend. One place to rotate keys. One place to add a fallback. The gateway paid for itself the first time I avoided a week of scattered integration work. My life is 10 times easier when model switching is a routing rule instead of a codebase search.

There is a related category that causes some confusion. An LLM gateway is an operating layer for traffic that a company already sends. It provides routing, policy, credentials, observability, and sometimes caching or request transformation. The company can connect it to hosted APIs, local deployments, or both.

An inference marketplace is a supply and discovery layer. It brings together models, providers, prices, capacity, and sometimes a single billing relationship. A developer chooses among available inference products, while the marketplace handles the commercial and operational connection.

The two products are converging. A marketplace needs gateway features to route requests and enforce budgets. A gateway can expose a catalogue of providers and models that looks like a marketplace. The boundary will remain useful for describing the buyer's problem, even as the products share more plumbing.

I expect the gateway to become ordinary infrastructure for companies that run several AI workloads. The model will keep changing. The layer that controls access to models will become the stable part.

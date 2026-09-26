---
layout: single
title: "PII is becoming a propensity"
date: 2026-09-26 08:15:00 -0000
tags: [AI, Governance]
author: Yu Xi Chau
---

I suspect the definition of personally identifiable information will become stricter as AI lowers the cost of piecing together an identity. A recent paper, [Large-scale online deanonymization with LLMs](https://arxiv.org/abs/2602.16800), describes an agent that extracts clues from unstructured posts, searches for candidate identities, and reasons over the evidence. The researchers report that the system can re-identify people across platforms with high precision and operate at a scale that would be impractical for a human investigator.

We often treat PII as a category: a name or identity document is PII, while an isolated comment is not. That boundary is becoming less useful. The better question is the propensity that a piece of information, combined with other available information, can be stitched back to a person. AI changes that propensity by making search, extraction, and comparison cheap. Over the medium term, I expect governance bodies to take a stricter view of data that looks harmless on its own but becomes identifying when an agent can assemble the surrounding clues. ([paper summary from the authors](https://simonlermen.substack.com/p/large-scale-online-deanonymization))

---
layout: single
title: "The prompt is the hammer"
date: 2026-11-25 09:00:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

Lauren Tan's talk reached me through [Yarchi's clip](https://x.com/undefinedKi/status/2121706023950090340) of the AI Engineer Code Summit, and the part I keep thinking about is her rule for agent mistakes: each one becomes a lint rule instead of a line in the prompt. Tan works on GrokBot at SpaceXAI. Her agents check their own work with tests, screenshots and videos, and the clip reports 3,000 PRs to production in a month, with the codebase clean enough that agents now merge most of their own PRs. That runs against what most teams reach for first. Hold a hammer and everything starts looking like a nail, and for anyone building with coding agents the prompt is that hammer. Editing the system prompt takes a minute and you can watch the effect in the next run. A lint rule takes more work. You have to write it, it lives in the repo, and it constrains every future run instead of the one in front of you.

Ilya Sutskever gave the wider version of that feeling its clearest voice. At NeurIPS in 2024 he argued that [pre-training as we knew it would end](https://www.youtube.com/watch?v=1yvBqasHLZs) because the internet had run out of new data, and plenty of people heard a plateau coming. We had one lever in view while the rest of the toolbox sat unused, and the answer turned out to rest on inference-time reasoning as much as anything else. The harness directions teams are converging on now look like the same correction at a smaller scale. People I have been reading are dropping lossy context compaction for file-backed retrieval, and splitting long-context drafting from zero-history review. Tan's lint rules handle a class of failure inside the repo; those two handle memory and review bias. Squeeze one lever dry and you end up doing the work you always knew was there.

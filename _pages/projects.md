---
layout: single
title: Projects
permalink: /projects/
classes: wide
---

A running list of things I build in my spare time. Each project gets a page with the actual working artifact, not just a description, so you can poke at the results yourself.

## LLM Model Analysis

<figure style="margin:0 0 1rem;">
  <a href="/projects/llm-model-analysis/"><img src="/assets/images/projects/llm-intelligence-cost.png" alt="LLM Intelligence vs Cost scatter chart" style="border:1px solid #d0d7de; border-radius:8px; max-width:100%;"></a>
</figure>

I spend my working life picking LLMs for production workloads, and the gap between benchmark rank and real-world cost is bigger than most model cards admit. This page takes the top 50 models in the [Artificial Analysis](https://artificialanalysis.ai) Intelligence Index (v4.1) and plots intelligence against the actual cost per task, with filters for lab, reasoning mode, effort level, and a minimum intelligence cutoff.

**What I'm exploring:** frontier labs price reasoning effort at wildly different rates for similar scores. The scatter makes the value outliers obvious, and the best-value card on the page does the arithmetic for you.

[Open the dashboard →](/projects/llm-model-analysis/)

---

## Hong Kong Rental Index Explorer

<figure style="margin:0 0 1rem;">
  <a href="/projects/hk-rent-index/"><img src="/assets/images/projects/hk-rent-index.png" alt="Hong Kong private domestic rental index chart, 1979 to 2026" style="border:1px solid #d0d7de; border-radius:8px; max-width:100%;"></a>
</figure>

The Rating and Valuation Department has published a territory-wide rental index for private domestic flats since 1979, but the raw spreadsheets bury the story. This page plots the full series, monthly from 1993 and quarterly before that, with period presets (5/10/15/20 years or everything) and custom start/end pickers. Whatever window you choose, the chart rebases so the first observation is 100, which turns forty-plus years of index points into one honest answer: what did rents do since then?

**Why I built it:** I kept wanting to answer a simple question, "how do today's rents compare with 1997, or 2003, or 2019?", and every source either showed a five-year window or made me do the arithmetic myself.

[Open the explorer →](/projects/hk-rent-index/)

---

## Sumo Elo History (All Divisions)

<figure style="margin:0 0 1rem;">
  <a href="/projects/sumo-elo/"><img src="/assets/images/projects/sumo-elo.png" alt="Sumo Elo explorer with Hakuho, Terunofuji, Aonishiki and Kotozakura curves" style="border:1px solid #d0d7de; border-radius:8px; max-width:100%;"></a>
</figure>

Every honbasho bout from March 1958 to July 2026 replayed through an Elo engine, all six divisions, 9,048 rikishi, 748,204 bouts. Each rikishi starts from a seed rating based on the division they first appeared in, then moves bout-by-bout with K=64. Withdrawals and forfeit wins are excluded, and there is no decay, so the rating pool is conserved across the full 68-year history.

**What you can do:** search any rikishi and overlay their career curve against anyone else's, slide the time window to read the leaderboard at any point in history, and filter by division. The top-ten highest ratings ever recorded are all here: Hakuho at 3,773, then Harumafuji, Asashoryu, Kakuryu, Terunofuji and the rest.

**Why I built it:** sumo fans argue about who was strongest all the time, and there is no objective record. Elo gives every rikishi and every era one comparable number.

[Open the dashboard →](/projects/sumo-elo/)

---

*More projects coming. I'm also working on a private essay-summarisation pipeline and a church worship site, and will document them here as they stabilise.*
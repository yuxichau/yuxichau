---
layout: single
title: "An Elo rating for every rikishi since 1958"
date: 2026-08-25 09:00:00 -0000
tags: [Sumo, Data, Projects]
author: Yu Xi Chau
---

I built an Elo rating for every rikishi who competed since 1958. The dashboard is live at [yuxichau.com/projects/sumo-elo/](/projects/sumo-elo/).

**Data.** Every honbasho bout from March 1958 to July 2026, pulled from sumo-api.com. 748,204 bouts across 409 tournaments, 9,048 rikishi, all six divisions.

**Method.** Standard Elo with K=64 and scale 400, replayed day by day in chronological order. Each rikishi starts from a seed based on the division they first appeared in, from yokozuna at 2800 down to jonokuchi at 1500. Withdrawal days and fusen wins are excluded, so neither side moves when a bout is forfeited. There is no decay: an absent rikishi keeps their rating, which keeps the total pool conserved across the whole history.

One honest caveat on coverage. Makuuchi and juryo have full bout records from 1958. The four lower divisions only have bout-level records from January 1988, since only aggregate wins and losses were published before that. Those rikishi hold their seed rating until 1988 or until they reach a sekitori division. The dashboard documents this in its methodology section.

**Top 10 highest Elo ever recorded:**

| # | Rikishi | Peak Elo | Achieved |
|---|---|---|---|
| 1 | Hakuho | 3773 | Sep 2010 |
| 2 | Harumafuji | 3610 | Sep 2012 |
| 3 | Asashoryu | 3580 | Jan 2007 |
| 4 | Kakuryu | 3570 | Mar 2014 |
| 5 | Terunofuji | 3524 | Nov 2021 |
| 6 | Baruto | 3523 | Mar 2010 |
| 7 | Kisenosato | 3499 | May 2016 |
| 8 | Goeido | 3484 | Sep 2016 |
| 9 | Kotoshogiku | 3476 | Jan 2016 |
| 10 | Onosato | 3445 | May 2025 |

Hakuho holds the all-time peak at 3,773, reached during the September 2010 tournament. Nine of the ten peaks fall in the 2000s and 2010s. The only current top-ten name is Onosato, whose peak came at the May 2025 basho.

The fun part is the comparison tool. Pick any two rikishi, overlay their career curves, and slide the window to read the leaderboard as of any tournament in history.
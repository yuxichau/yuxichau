---
layout: single
title: "Revisiting explosive condensation"
date: 2026-09-14 10:00:00 -0000
tags: [Projects]
author: Yu Xi Chau
---

Today I revised the explanation of my [explosive condensation project](https://yuxichau.com/projects/explosive-condensation/). The paper, ["Explosive condensation in symmetric mass transport models"](https://arxiv.org/abs/1508.07516), was largely my PhD work, and the interactive page gave me a reason to return to it properly. I am forever thankful to my supervisors, Stefan Grosskinsky and Colm Connaughton, for their guidance and patience during that period.

I had help from GPT 6 Astra in creating the new explanation. It was much better than a previous version I had written, so I decided to replace that version completely. What Astra did especially well, compared with other models I have tried, was hold a storytelling narrative across a long piece of technical work. It is almost as if it has two minds: one tracking the local details and another reasoning over the argument across a much longer span. The result was noticeably better, and arguably better than Opus 5. Fable 5.1 is so expensive that I have not used it enough to make a serious comparison.

One memory from the PhD is the code. I wrote it in C++ because Interacting Particle Systems become computationally demanding when a large cluster starts to form. The scaling behaviour only becomes visible when the lattice is sufficiently large. I was stuck for a while until I found an approximation: instead of treating a large cluster as one object, I approximated its motion on a symmetric lattice as a random walk. That made the calculation manageable and let me get back to the question the simulation was supposed to answer.

I do not see many people replicating this work, which probably means it is not very interesting anymore. That is one of the awkward truths about research. A technically correct result can still lose its audience when the question no longer feels alive. Research depends on asking interesting questions, and on sensing what might become interesting before it is obvious to everyone else.

The project page is now a small record of that earlier chapter, as well as an interactive way to see the model behave. I encourage people to turn their papers into interactive sites when they can. Watching a condensate form is more informative than reading a paragraph about it, and the exercise forces you to explain the mechanism clearly enough for somebody else to play with it.

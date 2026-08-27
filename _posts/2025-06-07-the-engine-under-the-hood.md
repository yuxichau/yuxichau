---
layout: single
title: "The Engine Under the Hood"
date: 2025-06-07 10:00:00 -0000
tags: [Technology]
author: Yu Xi Chau
---

In most companies running a generative AI programme, I'm the person people send when they can't decide which model to pick. The question comes around every few months, dressed up differently each time. "Is OpenAI still the answer?" "Should we move to Gemini?" "Why do the competitors keep changing?" Underneath, they're all the same question, and it isn't about which chatbot is smarter. It's about what it costs to run the thing you actually do.

The part people usually skip is the engine. The model is what gets the press, but the price you pay is set by the hardware it runs on. And the company that quietly decided to build its own hardware a decade ago is the one that keeps showing up at the cheap end of every leaderboard.

The LMSYS Chatbot Arena ranks models by blind tests, and the Gemini family is all over it. The small Gemma models, Flash at the fast and inexpensive middle, Pro at the top. At every tier, the pattern holds: Google's models deliver more for less than comparable alternatives. The whole lineup is arranged that way on purpose.

The obvious question is how. The answer sits underneath the models, in the engines they run on.

Run AI at any serious scale and you end up paying a tax to NVIDIA. Their GPUs are the only realistic option, so they set the price, and it is priced as the only realistic option. The hardware itself is excellent. That is exactly why the tax holds.

Google made a different bet more than a decade ago: build its own chip. The Tensor Processing Unit is vertical integration in the mould of Apple, where the people who design the silicon also decide what runs on it. Google did not rent a factory, it built one, and it designed every machine inside.

The design philosophy matters as much as the engineering. A GPU is a general-purpose engine: graphics, scientific computing, AI. A TPU is built for one job, running neural networks. Neural networks, under the hood, are mostly a long series of matrix multiplications, tensors multiplied together over and over again. Google's TPUs remove everything that is not that one operation and perfect the Matrix Multiply Unit at the centre of the chip. Instead of a sedan that hauls anything, you get a race car built for one track.

The specialization runs deeper. Modern models deal in sparse tensors. Pull one user's viewing history from billions of hours of YouTube and you get an enormous array where almost every entry is zero, because they have not watched that video. A general-purpose chip multiplies those zeros anyway, spending power and time on nothing. Google's SparseCores are built to skip the zeros and compute only the entries that matter. That is the quiet reason Google Search and Ads run at planetary scale without the compute bill swallowing the company.

The newer generations, Trillium and Ironwood, push the same direction: more memory, more efficiency at the workloads becoming AI's biggest bottleneck. Faster, and also cheaper per unit of useful work, and the second number is the one that decides what AI products can cost.

So while the industry argues about which model writes the better email, the contest underneath is about economics. Most companies in the AI race buy their fuel from a single supplier. Google owns the refinery.

I think the TPUs are structurally good. The engineering choices, the specialization in training and inference, the refusal to be a general-purpose anything, add up to something real. And I say that hoping I am wrong. Not because I want Google to fail, but because a field with room for many engines is a more interesting field than one where the answer was settled years ago. So far nobody has managed to unsettle it, and I keep half-waiting for someone to.

---

*Post-script, added later.*

I wanted to come back to this, because the thesis got tested in the field sooner than I expected. We were processing general medical documents, the kind every insurer handles: clinical letters, referral forms, lab reports, scans of pages that were never born digital. The incumbent approach was Microsoft's Content Understanding, which had grown a semantic layer and an LLM integration over the years, and the ledger showed it: it was expensive, and the price kept climbing as Microsoft modernised it.

Then we pointed Gemini 3 Flash at the same stack of documents. Zero-shot, no retraining, no custom extractor. It read the medical documents better than the specialised document service — better than the OCR-plus-semantics pipeline we had been paying for — at about half the cost.

That is the part I find worth sitting with. A general-purpose model, pointed at a job a specialised tool was built for, and it won on both quality and price. It does not mean TPUs are right for everyone, and it does not mean the specialised tools are doomed. It means the field is more open than the consensus assumes, which is exactly what I said I was hoping for. I got my wish sooner than I expected to.
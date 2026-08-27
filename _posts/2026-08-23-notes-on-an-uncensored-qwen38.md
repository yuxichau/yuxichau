---
layout: single
title: "Notes on an uncensored Qwen3.8"
date: 2026-08-23 09:00:00 -0000
tags: [AI]
author: Yu Xi Chau
---

Orca Router dropped uncensored weights of Qwen3.8-27B on Hugging Face this week: [full precision](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored) (gated), plus open [GGUF](https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-GGUF), FP8, and MLX builds. The GGUFs pulled six figures of downloads in days. This is an abliterated model: refusal behavior removed straight from the weights, no retraining, and by most accounts the surgery worked, virtually censoring nothing while keeping the base model coherent.

Abliteration rests on a finding from two years ago. [Arditi et al. 2024](https://arxiv.org/abs/2406.11717) showed that refusal in chat models is mediated by a single direction in the residual stream. Take the difference in activations between harmful and harmless prompts, find that direction, then orthogonalize the weight matrices against it so the model can no longer express refusal. It is a striking example of how sophisticated we have become at studying localized phenomena inside large complex structures: billions of parameters, and the behavior lives along one axis. The analysis still takes hours, up to nine by some accounts for a model this size, but from this point onwards that cost only goes down.

There is a parallel worth noting in neuroscience. Deep brain nuclei behave something like refusal vectors. Sensory data funnels and compresses through the amygdala, and when the pattern reads as threat, a whole-body response fires: freeze, flee, fight. The basal ganglia play the same trick on actions, gating movement plans through go and no-go pathways. Low-dimensional bottlenecks deciding what the rest of the system may express.

The name gives the game away. Abliteration comes from ablation, a real and widely used neurosurgical technique. For drug-resistant epilepsy or Parkinson's, surgeons can now destroy misbehaving tissue instead of opening the skull: stereotactic laser ablation threads a thin optical fiber through a burr hole and heats the seizure focus, often in the hippocampus or amygdala itself, under real-time MR thermometry, while MRI-guided focused ultrasound passes hundreds of beams harmlessly through the skull and lets them converge at one point in the thalamus, hot enough there to quiet a tremor circuit. Or surgeons leave the tissue alive and plant electrodes in a bottleneck like the subthalamic nucleus, sending current to dampen or shift its output. That last option, modulation rather than destruction, is closest in spirit to what abliteration does to a model: remove the signal, keep the structure. Deep learning borrowed the term from medicine, as it tends to.

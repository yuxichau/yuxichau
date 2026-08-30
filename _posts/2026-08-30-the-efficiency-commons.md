---
layout: single
title: "The Efficiency Commons"
date: 2026-08-30 08:30:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

# The Efficiency Commons

Tencent compressed [Hy4-preview](https://github.com/Tencent-Hunyuan/Hy4-preview), its open-weights 770B model, from 1.5TB to about 200GiB of GGUF, over seven times smaller. The scheme, [MIX-STQ1_0](https://x.com/TencentHunyuan/status/2093572224342954019), lets calibration data pick each layer's bit width: tolerant layers drop to 1.31 bits as sparse ternary, sensitive ones keep 2.06 bits, and the benchmarks barely move. The result runs in llama.cpp, on hardware that could never hold a terabyte and a half of weights.

This is the sequel to the [quant quality ladder](/posts/the-quant-quality-ladder/), where a 27B model fell off a cliff at 1.8 bits. The caveat there: architecture reshapes where the cliff sits. A 770B MoE with per-layer allocation is the demonstration. MoE redundancy buys back precision a dense model cannot spare.

Frontier-class models are now built in three steps.

The first step is the architecture, shaped by two pressures: memory and signal. Mixture of experts keeps knowledge large while active parameters stay small. Latent attention and the KV-cache family, the [MLA trick from DeepSeek-V2](https://arxiv.org/abs/2405.04434), shrink the memory that context eats. Linear attention with sparse indexers avoids attention's quadratic bill; position encodings, routing and objectives push computation to do more per token. Efficiency is decided here, before training starts.

The second step is training in relatively high precision, BF16 or FP8, so the capability reaches its ceiling. It is the conservative step, and rightly so: precision is insurance, and nobody wants noisy gradients because they were cheap.

The third step is compression. The model already knows what it knows; the job is to make it cheap to run and easy to move. Quantization from 8-bit down to the 1.3-bit class, sometimes extremely precise, as with Tencent's per-layer allocation. Distillation, pruning, everything that ends in a [GGUF](https://github.com/ggml-org/llama.cpp) someone can download.

The pattern I keep noticing: the interesting innovation happens in steps one and three, led by the open-source ecosystem. DeepSeek's MoE and latent attention, Qwen and GLM shipping architecture in the open, the llama.cpp quant formats and their [AWQ](https://github.com/mit-han-lab/llm-awq)/GPTQ lineage, ternary quantization, Hy4 itself under Apache 2.0. Step two is where the money goes and where the least is published: data and training runs stay private.

Which brings me to the point of this post. Nothing stops proprietary models from adopting any of this. The step-one ideas are in papers and code; the step-three tricks ship under permissive licenses and can fold into a closed serving stack within a quarter. Some already did: FP8 inference and NVFP4 are standard at the big hosts.

The efficiency frontier is a commons. Every squeeze an open lab publishes raises the floor for everyone, including labs that never share back. That is the durable contribution of open weights: a rising floor, not an exclusive cost advantage. The techniques are public, so the gap keeps closing; the durable differences sit in data, training scale and product.

It is the good kind of race: each trick gets tested by thousands of people on their own hardware the moment it lands, which is how a 200GiB frontier model becomes a download instead of a machine-room decision. Less secrecy, more floor, and the floor is what the rest of us stand on.
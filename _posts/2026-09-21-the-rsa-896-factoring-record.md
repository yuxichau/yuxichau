---
layout: single
title: "The RSA-896 factoring record is impressive, but the panic is misplaced"
date: 2026-09-21 12:00:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

On 3 September, Eric Lu at Cognition factored RSA-260, an 862-bit challenge number, with a GPU-accelerated version of CADO-NFS and help from Devin. On 19 September, Anthropic engineer Stephen A. Weis announced the factorisation of RSA-896, a 896-bit challenge number, with help from Claude. The [RSA-896 challenge](https://mysterytwister.org/media/challenges/pdf/mtc3-rsa-10-en.pdf) is a public semiprime, so the result can be checked by multiplying the two published prime factors back together. The speed of the two records is the part I find unsettling: specialist cryptographic work that once demanded a large research effort can now be attacked with an AI agent coordinating the engineering around an established algorithm. [Lu's account of RSA-260](https://cognition.com/blog/factoring-rsa-260) makes the same point from the other side.

There is no reason to treat this as the sudden collapse of RSA-2048. An 896-bit challenge number and a deployed 2048-bit modulus are very different workloads, and the public results do not introduce a new factoring algorithm. The practical response is more ordinary: review old keys, stop treating legacy RSA sizes as harmless, and keep migrating towards post-quantum schemes such as [NIST's ML-KEM](https://csrc.nist.gov/pubs/fips/203/final) where the system's threat model requires it. What has changed is the speed at which the engineering barrier can fall. That is the part security teams should watch closely.

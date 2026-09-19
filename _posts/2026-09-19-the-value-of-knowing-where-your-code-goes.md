---
layout: single
title: "The Value of Knowing Where Your Code Goes"
date: 2026-09-19 10:00:00 -0000
tags: [AI, Technology]
author: Yu Xi Chau
---

A story circulating on X alleges that Z.ai's ZCode desktop coding app quietly packages a user's workspace, including much of its `.git` history, LFS objects and reflogs, encrypts the bundle, and uploads it to Aliyun OSS. The [reverse-engineering report](https://merchmindai.net/blog/en/post/zcode-silent-git-history-upload) claims that the server retains the decryption key and that the app offers no clear switch to stop the capture. If those findings are accurate, this would be a clear violation of the terms users were entitled to rely on: collect what is needed to perform the task, explain what leaves the machine, and give the user a real choice. The issue is not that an AI coding agent needs access to code. The issue is silently taking a much larger copy, including material the user may believe they deleted or never intended to share.

This also makes GitHub Copilot's position look stronger. GitHub already stores the repositories that developers deliberately push to it, including most of the Git history and, where enabled, LFS objects. That gives Microsoft a natural reason to own GitHub, and makes its [2018 acquisition for $7.5 billion in Microsoft stock](https://news.microsoft.com/source/2018/06/04/microsoft-to-acquire-github-for-7-5-billion/) look more valuable in hindsight than it did at the time. GitHub became the place where source code, developer identity, workflows and now AI assistance meet. The advantage is not that Microsoft has no access to code. It is that the boundary is more visible and purposeful. The AI competition makes it essential to ask whether companies are being honest about that boundary. At the same time, more of this behaviour is coming into the sunlight because AI tools give users a reason to inspect what their computers are doing, and reverse-engineering is becoming cheap enough that misleading product claims are harder to hide.

---
layout: single
title: Projects
permalink: /projects/
classes: wide
description: "A catalogue of Yu Xi Chau's AI, data, mathematics, history, and browser-based projects, with working artifacts and methods."
---

A running list of working artifacts—dashboards, interactive audits, mathematical instruments, and browser experiments. Each page includes the live tool and its assumptions.

{% assign categories = site.data.projects | map: "category" | uniq %}
{% for cat in categories %}
<h2 class="sj-projects-cat">{{ cat }}</h2>
<div class="sj-projects-grid">
  {% assign items = site.data.projects | where: "category", cat %}
  {% for p in items %}
  <article class="sj-project-card">
    <span class="sj-project-card__meta">{{ p.tag }}</span>
    <h3 class="sj-project-card__title"><a href="{{ p.url | relative_url }}">{{ p.title }}</a></h3>
    <p class="sj-project-card__desc">{{ p.summary }}</p>
    <a class="sj-project-card__cta" href="{{ p.url | relative_url }}">Open project →</a>
  </article>
  {% endfor %}
</div>
{% endfor %}

<p class="sj-disclaimer" style="margin-top:2rem;">More projects in progress—including an essay-summarisation pipeline and a church worship site, to be documented here once stable.</p>

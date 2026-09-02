---
layout: default
title: Writing
permalink: /blog/
description: "Notes and write-ups by Md Miadul Islam Nizzan on AI/ML, NLP, and software engineering."
---

# Notes from the workbench.

Ideas, experiments, and lessons from building intelligent systems and learning computer science.

<div class="writing-list">
{% for post in site.posts %}
  <article class="writing-item">
    <p class="eyebrow">{{ post.date | date: "%B %Y" }}{% if post.categories.size > 0 %} · {{ post.categories | join: " / " }}{% endif %}</p>
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.description | default: post.excerpt | strip_html | truncatewords: 32 }}</p>
    <a class="text-link" href="{{ post.url | relative_url }}">Read article <span>→</span></a>
  </article>
{% else %}
  <article class="writing-item"><p class="eyebrow">Coming soon</p><h2>First field note in progress.</h2><p>I’m preparing practical notes on machine learning experiments, network systems, and the engineering lessons behind my projects.</p></article>
{% endfor %}
</div>

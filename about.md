---
layout: page
title: "About Me"
permalink: /about/
description: "Learn about my background, interests, and what drives my work in AI/ML and software engineering."
---

I'm {{ site.name }}, a Computer Science and Engineering undergraduate at Green University of Bangladesh with a strong academic record and project experience spanning artificial intelligence, machine learning, natural language processing, computer vision, multi-agent systems, software engineering, networking, and embedded systems.

## Background

I'm currently pursuing my B.Sc. in Computer Science and Engineering, expected January 2027, with a current CGPA of 3.70 / 4.00. I've been recognized with both the Vice Chancellor's Award and the Dean's Award for academic performance at Green University of Bangladesh.

Beyond coursework, I serve as **Vice Chair of the IEEE GUB Student Branch** and as a **Student Mentor**, guiding junior students through academic planning, technical coursework, and project work.

## Research interests

Bangla natural language processing; social-media safety and online-harassment detection; retrieval-augmented generation; intelligent agents; computer vision; trustworthy and explainable AI; federated learning; AI for cybersecurity; network security.

## Current work

- **Undergraduate thesis** — Robustness, explainability, and attribution stability of lightweight vision transformers for federated chest X-ray classification under non-IID client distributions.
- **Manuscript submitted** — Robustness and tokenization stability of transformer models for 12-class Bangla dialect classification under character-level perturbations, submitted to the 2026 IEEE 8th International Conference on Sustainable Technologies for Industry 5.0 (STI).
- **Research in progress** — Multilevel detection of social media harassment targeting women, including dataset curation and text-classification model fine-tuning.

[See the full research page →]({{ '/research/' | relative_url }})

## Education

<div class="timeline">
{% for entry in site.data.education %}
  <div class="timeline-item">
    <p class="timeline-meta">{{ entry.year | default: entry.status }}</p>
    <h3>{{ entry.degree }}</h3>
    <p>{{ entry.institution }} — {{ entry.location }}{% if entry.cgpa %} · CGPA {{ entry.cgpa }}{% endif %}{% if entry.gpa %} · GPA {{ entry.gpa }}{% endif %}</p>
  </div>
{% endfor %}
</div>

## Leadership & mentorship

<div class="timeline">
{% for role in site.data.experience %}
  <div class="timeline-item">
    <p class="timeline-meta">{{ role.start_date }} – {{ role.end_date }}</p>
    <h3>{{ role.title }} · {{ role.organization }}</h3>
    <p>{{ role.description }}</p>
  </div>
{% endfor %}
</div>

## Awards & recognition

<div class="timeline">
{% for award in site.data.awards %}
  <div class="timeline-item">
    <p class="timeline-meta">{{ award.organization }}{% if award.year %} · {{ award.year }}{% endif %}</p>
    <h3>{{ award.title }}</h3>
    <p>{{ award.description }}</p>
  </div>
{% endfor %}
</div>

## What drives me

I believe technology should solve genuine problems — whether that's helping farmers identify crop disease early, making AI models more explainable, or improving safety on social platforms. I value clear communication, rigorous thinking, and the collaborative spirit of open-source and research communities.

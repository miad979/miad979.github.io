---
layout: page
title: "Resume / CV"
permalink: /resume/
description: "My professional resume and curriculum vitae."
---

<div class="resume-head">
<h2>{{ site.name }}</h2>
<p class="resume-role">{{ site.role }}</p>
<p class="resume-contact">{{ site.email }} · {{ site.phone }} · {{ site.location }}</p>
<p class="resume-contact"><a href="{{ site.github_url }}">GitHub</a> · <a href="{{ site.linkedin_url }}">LinkedIn</a> · <a href="{{ site.ieee_url }}">IEEE Collabratec</a></p>
</div>

<div class="resume-actions">
  <a class="button button-primary" href="{{ site.resume_pdf | relative_url }}" target="_blank" rel="noopener">Download PDF</a>
</div>

---

## Professional summary

Computer Science and Engineering undergraduate with a strong academic record (3.70/4.00 CGPA) and project experience spanning artificial intelligence, machine learning, natural language processing, computer vision, multi-agent systems, software engineering, networking, cybersecurity, and embedded systems. Combines research-oriented development with student mentoring, IEEE leadership, and collaborative technical initiatives.

## Education

<div class="timeline">
{% for entry in site.data.education %}
<div class="timeline-item">
<p class="timeline-meta">{{ entry.year | default: entry.status }}</p>
<h3>{{ entry.degree }}</h3>
<p>{{ entry.institution }} · {{ entry.location }}{% if entry.cgpa %} · CGPA {{ entry.cgpa }}{% endif %}{% if entry.gpa %} · GPA {{ entry.gpa }}{% endif %}</p>
</div>
{% endfor %}
</div>

## Undergraduate thesis (ongoing)

**Robustness, Explainability, and Attribution Stability of Lightweight Vision Transformers for Federated Chest X-ray Classification under Non-IID Client Distributions** — Green University of Bangladesh, 2026 – present.

## Manuscript submitted

**Robustness and Tokenization Stability of Transformer Models for 12-Class Bangla Dialect Classification Under Character-Level Perturbations** — submitted to the 2026 IEEE 8th International Conference on Sustainable Technologies for Industry 5.0 (STI); decision pending.

## Technical expertise

| Category | Skills |
| :--- | :--- |
{% for group in site.data.skills %}| **{{ group.category }}** | {{ group.skills | join: ", " }} |
{% endfor %}

## Experience & leadership

<div class="timeline">
{% for role in site.data.experience %}
<div class="timeline-item">
<p class="timeline-meta">{{ role.start_date }} – {{ role.end_date }}</p>
<h3>{{ role.title }} · {{ role.organization }}</h3>
<p>{{ role.description }}</p>
</div>
{% endfor %}
</div>

## Awards, membership & academic service

{% for award in site.data.awards %}- **{{ award.title }}** — {{ award.organization }}{% if award.year %} ({{ award.year }}){% endif %}: {{ award.description }}
{% endfor %}

## Academic references

1. **Mr. Syed Ahsanul Kabir** — Chairperson & Associate Professor, Department of CSE, Green University of Bangladesh
2. **Professor Dr. Md. Ahsan Habib** — Chairperson, Department of CSE, Bangladesh University of Business and Technology

Referee contact details are available on request — please [email me]({{ 'mailto:' | append: site.email }}).

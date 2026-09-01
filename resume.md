---
layout: page
title: "Resume / CV"
permalink: /resume/
description: "My professional resume and curriculum vitae."
---

**{{ site.name }}**
{{ site.role }}
📧 {{ site.email }} · 📱 {{ site.phone }} · 📍 {{ site.location }}

[GitHub]({{ site.github_url }}) · [LinkedIn]({{ site.linkedin_url }}) · [IEEE Collabratec]({{ site.ieee_url }})

<div class="resume-actions">
  <a class="button button-primary" href="{{ site.resume_pdf | relative_url }}" target="_blank">Download PDF</a>
</div>

---

## Professional summary

Computer Science and Engineering undergraduate with a strong academic record (3.70/4.00 CGPA) and project experience spanning artificial intelligence, machine learning, natural language processing, computer vision, multi-agent systems, software engineering, networking, cybersecurity, and embedded systems. Combines research-oriented development with student mentoring, IEEE leadership, and collaborative technical initiatives.

## Education

{% for entry in site.data.education %}
**{{ entry.degree }}** — {{ entry.institution }}
{{ entry.location }} · {{ entry.year | default: entry.status }}{% if entry.cgpa %} · CGPA {{ entry.cgpa }}{% endif %}{% if entry.gpa %} · GPA {{ entry.gpa }}{% endif %}

{% endfor %}

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

{% for role in site.data.experience %}**{{ role.title }}** — {{ role.organization }}
{{ role.location }} · {{ role.start_date }} – {{ role.end_date }}
{{ role.description }}

{% endfor %}

## Awards, membership & academic service

{% for award in site.data.awards %}- **{{ award.title }}** — {{ award.organization }}{% if award.year %} ({{ award.year }}){% endif %}: {{ award.description }}
{% endfor %}

## Academic references

1. **Mr. Syed Ahsanul Kabir** — Chairperson & Associate Professor, Department of CSE, Green University of Bangladesh · kabir@cse.green.edu.bd
2. **Professor Dr. Md. Ahsan Habib** — Chairperson, Department of CSE, Bangladesh University of Business and Technology · ahsan.habib.tareq@gmail.com

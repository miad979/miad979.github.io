---
layout: page
title: "Certifications & Training"
permalink: /certifications/
description: "Certifications and training."
---

{% if site.data.certifications and site.data.certifications.size > 0 %}
  {% for cert in site.data.certifications %}
<div class="portfolio-card">
  <h3>{{ cert.title }}</h3>
  <p>{{ cert.issuer }}{% if cert.year %} · {{ cert.year }}{% endif %}</p>
  {% if cert.url %}<div class="project-links"><a href="{{ cert.url }}" target="_blank" rel="noopener">View credential →</a></div>{% endif %}
</div>
  {% endfor %}
{% else %}
<div class="empty-state">
  <p>No certifications listed yet. Add entries to <code>_data/certifications.yml</code> and they'll appear here automatically.</p>
</div>
{% endif %}

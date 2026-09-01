---
layout: page
title: "Publications"
permalink: /publications/
description: "Manuscripts and academic publications."
---

{% assign manuscripts = site.data.research | where: "type", "Manuscript" %}
{% if manuscripts.size > 0 %}
  {% for item in manuscripts %}
<div class="portfolio-card">
  <span class="tech-badge">{{ item.status }}</span>
  <h3>{{ item.title }}</h3>
  <p>{{ item.description }}</p>
  {% if item.submit_date %}<p><strong>Venue:</strong> {{ item.submit_date }}</p>{% endif %}
</div>
  {% endfor %}
{% else %}
<div class="empty-state">
  <p>No publications yet — this page will update automatically once a manuscript entry is added to <code>_data/research.yml</code>.</p>
</div>
{% endif %}

[Ask about my research](mailto:{{ site.email }}?subject=Research%20work){: .button .button-primary }

---
layout: default
title: Blog
permalink: /blog/
---

# Tech || Research || Adventure

Welcome to my engineering and problem-solving notebook. Here, I break down algorithmic challenges, structural complexity optimizations, and development strategies.

---

<div class="blog-posts-feed-container" style="margin-top: 30px;">
  {% for post in site.posts %}
    <div class="blog-post-card" style="background: var(--bg-card, #1e1e1e); border: 1px solid var(--border-color, #333); border-radius: 8px; padding: 25px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
      
      <div class="post-meta" style="font-family: monospace; font-size: 12px; color: var(--text-muted, #888); margin-bottom: 12px;">
        📅 {{ post.date | date: "%B %d, %Y" }}
        {% if post.categories.size > 0 %}
          • 🏷️ 
          {% for category in post.categories %}
            <span style="background: rgba(0, 122, 204, 0.1); color: #007acc; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-right: 4px;">#{{ category }}</span>
          {% endfor %}
        {% endif %}
      </div>

      <h2 style="margin: 0 0 15px 0; border: none; padding: 0;">
        <a href="{{ post.url | relative_url }}" style="text-decoration: none; font-size: 24px; font-weight: 700; color: var(--text-main, #fff); transition: color 0.2s ease;">
          {{ post.title }}
        </a>
      </h2>

      <p style="color: var(--text-main, #fff); font-size: 15px; line-height: 1.6; margin-bottom: 20px; font-style: italic;">
        {{ post.description }}
      </p>

      <div class="blog-structure-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 6px; border-left: 3px solid #007acc;">
        <div class="grid-block">
          <strong style="color: #ff4a4a; display: block; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">❓ The Challenge</strong>
          <span style="font-size: 13px; color: var(--text-muted, #888);">Algorithmic logic, constraints analysis, and sample case tracking.</span>
        </div>
        <div class="grid-block">
          <strong style="color: #007acc; display: block; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">💡 Strategy</strong>
          <span style="font-size: 13px; color: var(--text-muted, #888);">Data structures selection, optimization formulas, and time-space tradeoffs.</span>
        </div>
        <div class="grid-block">
          <strong style="color: #28a745; display: block; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">💻 Solution</strong>
          <span style="font-size: 13px; color: var(--text-muted, #888);">Clean, fully-commented implementation with line-by-line breakdowns.</span>
        </div>
      </div>

      <div style="margin-top: 20px; text-align: right;">
        <a href="{{ post.url | relative_url }}" style="display: inline-block; background: #007acc; color: #fff; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-size: 13px; font-weight: 600; transition: background 0.2s;">
          Explore Solution Matrix →
        </a>
      </div>

    </div>
  {% else %}
    <p style="color: var(--text-muted); font-style: italic;">No blog entries published yet. Stay tuned!</p>
  {% endfor %}
</div>

---
layout: default
title: Roadmap
---
# Learn Python 3, one topic at a time

Each topic has three pages: **Learn** (key points and examples), **Test** (10 multiple-choice questions with instant feedback) and **Assignments** (3 to 5 coding tasks with starter code, tests and a hidden solution).

The course targets **Python 3.14 or later**. The order follows [*Introducing Python*](https://www.oreilly.com/library/view/introducing-python-3rd/9781098174422/) and the practice style of *Learn Python the Hard Way*: read a little, type code yourself, and check it.

<ol class="roadmap">
{% for m in site.data.modules %}
  <li class="{% if m.status != 'ready' %}soon{% endif %}">
    <span class="num">{{ forloop.index }}</span>
    <div class="body">
      <strong>{{ m.title }}</strong>
      <small>{{ m.summary }}</small>
      {% if m.status == 'ready' %}
      <span class="links">
        <a href="{{ '/modules/' | append: m.slug | append: '/' | relative_url }}">Learn</a>
        <a href="{{ '/modules/' | append: m.slug | append: '/quiz/' | relative_url }}">Test</a>
        <a href="{{ '/modules/' | append: m.slug | append: '/assignments/' | relative_url }}">Assignments</a>
        <span class="badge" data-badge="{{ m.slug }}"></span>
      </span>
      {% else %}
      <small>Coming soon</small>
      {% endif %}
    </div>
  </li>
{% endfor %}
</ol>

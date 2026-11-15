---
layout: default
title: Roadmap
---
# Learn Python 3, one topic at a time

Each topic has three pages: **Learn** (key points and examples), **Test** (10 multiple-choice questions with instant feedback) and **Assignments** (3 to 5 coding tasks with starter code, tests and a hidden solution).

The course targets **Python 3.14 or later**. The order follows [*Introducing Python*](https://www.oreilly.com/library/view/introducing-python-3rd/9781098174422/) and the practice style of *Learn Python the Hard Way*: read a little, type code yourself, and check it.

## Printable cheatsheets

<div class="cs-actions">
  <a class="btn" href="{{ '/cheatsheets/basic/' | relative_url }}">Basic cheatsheet (topics 1-25)</a>
  <a href="{{ '/assets/pdf/python-basic-cheatsheet.pdf' | relative_url }}" download>PDF</a>
  <a class="btn" href="{{ '/cheatsheets/advanced/' | relative_url }}">Advanced cheatsheet (topics 26-39)</a>
  <a href="{{ '/assets/pdf/python-advanced-cheatsheet.pdf' | relative_url }}" download>PDF</a>
</div>

## Part 1: Basics (topics 1-25)

<ol class="roadmap">
{% for m in site.data.modules limit: 25 %}{% include roadmap-item.html m=m %}{% endfor %}
</ol>

## Part 2: Advanced Python for modern applications (topics 26-39)

These topics use general examples (job runners, URL fetchers, log processing). Each ends with a short note on how the idea appears in AI agent code, and the last two topics build an agent.

<ol class="roadmap">
{% for m in site.data.modules offset: 25 %}{% include roadmap-item.html m=m %}{% endfor %}
</ol>

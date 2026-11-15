---
layout: default
title: Glossary
---
# Glossary

Terms are grouped by the topic that introduces them.

{% for m in site.data.modules %}{% assign terms = site.data.glossary[m.slug] %}{% if terms %}
## {{ m.title }}

<dl>
{% for t in terms %}<dt>{{ t.term }}</dt><dd>{{ t.meaning | markdownify | remove: "<p>" | remove: "</p>" }}</dd>
{% endfor %}</dl>
{% endif %}{% endfor %}

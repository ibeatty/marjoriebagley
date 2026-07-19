---
layout: page
title: Performances
permalink: /events/
---

{% include event-split.html %}

{% if upcoming.size > 0 %}
## Upcoming

{% include event-list.html events=upcoming show_blurbs=true %}
{% endif %}

## Past performances

{% include event-list.html events=past show_blurbs=false %}

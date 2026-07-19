---
layout: page
title: Performances
nav_title: Season
permalink: /events/
wide: true
---

{% include event-split.html %}

{% if upcoming.size > 0 %}
<section class="season-group">
<h2>Upcoming</h2>
{% include event-list.html events=upcoming show_blurbs=true %}
</section>
{% else %}
<p class="events-note">During the season, Marjorie performs in most Greensboro
Symphony Masterworks and Pops programs as concertmaster, appears in faculty
recitals at UNCG, and plays chamber music in North Carolina and beyond.
Dates for the coming season appear here as they are announced.</p>
{% endif %}

{% include season-archive.html events=past %}

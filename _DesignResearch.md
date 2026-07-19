# Design research: sites of comparable musicians

*July 2026. Survey of 14 personal sites of concertmaster/professor hybrids,
university violin faculty, chamber musicians, and (for contrast) star
soloists, to inform the redesign mockups in `mockups/`. Summary — details
were gathered live from each site.*

## Sites examined

frankalmond.com (ex-Milwaukee CM) · natesviolin.com (Nathan Cole, Boston CM —
teaching business, anti-model) · hollymulcahy.com (Wichita CM) ·
noahbendixbalgley.com (Berlin Phil 1st CM) · jessicamathaes.com (Austin CM +
faculty) · rachelleepriday.com (UW professor) · belenviolin.com (Michigan
professor) · itamarzorman.com (Indiana professor) · jenniferfrautschi.com
(Stony Brook) · alexikenney.com · paulhuangviolin.com · augustinhadelich.com ·
jamesehnes.com · hilaryhahn.com (404 — site simply down). Notably, several of
the *closest* comps (David Halen — SLSO CM + Michigan professor; David
Coucheron — Atlanta CM; Ara Gregorian — ECU) have **no personal site at all**;
and two chamber musicians' sites (Sussmann, Soovin Kim) have rotted at the
infrastructure level (dead certs/hosting).

## Genre conventions

1. Canonical nav: Bio · Schedule · Media · Press · Recordings · Contact.
2. Quote-led homepages (press blurbs as trust currency — needs only one good quote, ever).
3. Sans-serif monoculture (Raleway/Montserrat everywhere). The one serif site
   (Priday's Playfair/Crimson) instantly reads more distinguished.
4. Squarespace/Wix defaults, lightly customized (9 of 14).
5. White/near-black + one accent color (best: Paul Huang's single metallic gold).
6. Hybrids segment by ROLE, not media: Bendix-Balgley's nav is literally
   Soloist / Concertmaster / Klezmer / Chamber. Maps directly onto Marjorie's triad.
7. **Teaching is the genre's consistent hole**: of four professors surveyed,
   none has a page that actually addresses a prospective student. Our
   `studying.md` page is the differentiator — this survey validates it.

## Staleness patterns (ranked by how reliably they marked abandonment)

1. **Empty-state event widgets** — a calendar/upcoming section with nothing in
   it is the loudest possible abandonment signal. *Rule: no container whose
   empty state is publicly visible.* (Applied: home layout falls back to
   evergreen prose, never "no events listed.")
2. Frozen copyright years (© 2016, © 2019, © 2023 observed).
3. News/blog sections — every "News" page surveyed had a stale top item. Feeds demand feeding.
4. Event-of-the-moment nav items that never leave (a 2020 "Recitals from Home"
   still in a 2026 nav). Never name nav after a project or year.
5. Placeholder text left live ("Your Custom Text Here").
6. Homepage-as-social-media-pointer (site abandoned in spirit).
7. Infrastructure rot — lapsed Squarespace/Wix/certs. GitHub Pages + Jekyll
   actually beats the genre norm here.

## Opportunities (quiet deviations that stand out)

- **Editorial serif typography** in a sans-serif sea; typographic hero instead
  of photo hero (also solves the no-photo-pipeline constraint).
- **Actually address prospective students** in first person. Zero competition.
- **Season model, not rolling calendar**: "2026–27 Season" framing, grouped by
  role, updated once each August, honest for 12 months. (Our event collection
  can render this way — group by season label derived from date.)
- Evergreen "where to hear me" prose paragraph as the fallback/summary.
- An evergreen resources/"gift" page later (cf. Hadelich's free cadenza
  downloads): audition-rep guidance, practice notes, studio FAQ.
- An instrument/story page ("My Violin") — human, evergreen, rare.

## The five mockup directions

1. **Concert Program** *(maroon continuity)* — burgundy on warm ivory,
   hairline gold rules, high-contrast serif masthead set like a printed
   program title page; season page as a program listing.
2. **Ivory Editorial** — off-white/near-black, one accent; Playfair small-caps
   masthead + literary serif body; quote-or-sentence-led; dateless homepage.
3. **Conservatory Modern** — white/near-black/steel-blue; geometric sans,
   letterspaced caps nav; split hero (type left, single evergreen portrait
   right); three role cards: The Studio / The Orchestra / Chamber Music.
4. **Engraved Edition** — paper white + ink, burgundy whisper; EB Garamond/
   Cormorant set like a Henle/Bärenreiter title page; staff-line SVG rules;
   most austere.
5. **Piedmont Dusk** — deep spruce or ink-plum bands, warm cream body,
   terracotta accent; warm humanist serif (Lora/Alegreya); first-person
   two-sentence intro as the hero. Most distinctive while staying sober.

Cross-cutting rules for all: ≤6 nav items, no news/blog, no widget that can
render empty, dynamic copyright year, one evergreen portrait max, events
grouped by season.

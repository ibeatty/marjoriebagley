# Redesign Plan: Content Model & Information Architecture

*Phase 1 working document, July 2026. See `CLAUDE.md` for project context and constraints.*

> **Status (July 18, 2026):** Phases 1–2 are BUILT: `_events/` collection live
> with migrated concerts, upcoming/past templates, weekly cron rebuild,
> Makefile dev wrapper, Sveltia CMS at `/admin/` (auth steps pending — see
> `_SetupSveltia.md`), REST-API-based scraper with human-choice import.
> Phase 3 research is done (`_DesignResearch.md`) and NINE mockups await
> Marjorie's review (`mockups/index.html`): the original five, a violin-photo
> variant of front-runner #5 Piedmont Dusk (Ian's first impression, Jul 2026),
> and three wider-net directions (#6 Nocturne dark/amber, #7 Folio left-rail,
> #8 Overture indigo/ochre color-blocked) added after Ian observed #1/#2/#4
> clustered on the same warm-paper-serif theme. Remaining: Ian's manual steps
> in `_TODO.md`, design choice, then Phase 4 (implement chosen design as
> hand-rolled templates) and Phase 5 (content + DreamHost cutover).

## Guiding constraints (from project goals)

- Serve **two audiences synergistically**: prospective violin performance students (recruiting) and concert audiences.
- **Near-zero recurring upkeep.** Every page must look fine untouched for a year. No content types that go stale visibly (photography-driven heroes, "news," blog).
- Events are the *one* regularly-updated content type — so make updating them as frictionless as possible and make staleness invisible (old events age out automatically rather than sitting stale on the page).

## Content model

### Events (the core structured type)

Replace blog-post-shaped concert announcements (`_posts/`) with a structured **events collection** — one small YAML-front-matter file per event in `_events/`:

```yaml
---
title: "GSO Masterworks: Orchestral Fireworks!"
date: 2026-05-02            # concert date, not publication date
series: "GSO Masterworks"    # GSO Masterworks | GSO Pops | GSO | Chamber | UNCG | Other
role: ""                     # optional: "Soloist", "Concertmaster", "Guest artist" — shown only when notable
venue: ""                    # optional: "Tanger Center, Greensboro NC"
url: "https://greensborosymphony.org/event/..."
---
One- to three-sentence blurb. Body is optional.
```

Why this shape:

- **Upcoming/past is derived, not managed.** Templates split on `date` vs. build date. Upcoming events list ascending on the home/events page; past events fall into an archive automatically. Nothing to prune by hand.
- **Form-friendly.** A fixed field schema is exactly what a web form (CMS or issue-form) can populate — no free-form front matter.
- **Scraper-friendly.** The GSO import script writes the same schema; a human just approves/edits.
- `role` exists because Marjorie's involvement varies (concertmaster vs. featured soloist vs. chamber) and "soloist" events deserve visual emphasis.

**Staleness caveat + fix:** a static site only re-splits upcoming/past when rebuilt. Add a **scheduled GitHub Actions build** (weekly cron) so events age out even during no-edit stretches. Cheap, invisible, zero attention.

### Pages (evergreen prose)

Small fixed set; each must be writable once and left alone:

| Page | Audience | Status | Notes |
|---|---|---|---|
| Home | both | intro blurb drafted | Identity statement + upcoming events + clear paths to "Study" and "Bio" |
| Bio | both | drafted, has `XX` placeholders needing facts from Marjorie | The synergy narrative lives here |
| Studying with Marjorie | students | drafted; open question re private students flagged in red | The recruiting page: degree programs, application links, studio culture |
| Events | audiences | new | Full upcoming list + collapsed/linked past-events archive (past events double as an implicit performance résumé) |
| Listen *(optional)* | both | new | Discography (Equilibrium, Centaur, Albany, Summit, VOX) + a few performance videos. **Evergreen** — a discography never looks stale, so this satisfies the "richer content without upkeep" goal better than photos |
| Contact | both | new or footer-only | Email + existing social links; may not need its own page |

**Explicitly out:** a blog/news section (guaranteed staleness), photo galleries needing refresh, anything requiring seasonal rewrites.

### Navigation

Single flat nav, ≤5 items: **Home · Bio · Studying · Events (· Listen)**. Both audience paths visible from the home screen above the fold.

## Content-freshness audit of existing material

- `_posts/`: 5 leftover Minima demo posts from 2016 — delete. Real concert posts 2024–2026 → migrate into `_events/` schema (a one-time script can do this mechanically).
- `bio.md`: good draft; needs Marjorie to fill `XX` placeholders (ages, years) and the last-updated concert references (Lark Ascending, Thile duel) should either become evergreen phrasing or move to the events archive — dated "current highlights" in a bio are a staleness trap.
- `studying.md`: needs Marjorie's decision on the private-student question and her voice in the prose.
- `index.md`: intro blurb exists; will be reworked per chosen design.

## Decisions (Ian, July 2026)

- ✅ **Keep Jekyll; hand-roll minimal templates** (replace vendored Minima).
- ✅ **Sveltia CMS** for web authoring — go straight there (no Pages CMS trial). Needs: GitHub OAuth App + first-party Cloudflare Worker (free Cloudflare account), Marjorie's GitHub account as collaborator.
- ✅ **No email in use on @marjoriebagley.com** — hosting cutover is unblocked. (Aspiration: an alias forwarding to Marjorie's Gmail. Note: this does NOT require Google Workspace — free receive-only forwarding exists via DreamHost forward-only email, Cloudflare Email Routing, or ImprovMX.)

## Design ingredients: modern native CSS (from "BASELINE/26" reference)

Ian pointed to a "BASELINE/26" demo artifact cataloging what browsers now do natively, zero libraries — which aligns perfectly with the zero-dependency durability constraint. Techniques relevant to a *classy, understated* site (all degrade gracefully):

- **OKLCH color system** — perceptually uniform; derive a whole palette from one accent token via `oklch(from …)` relative syntax. One `--hue` variable = coherent, easily-tuned theme.
- **Scroll-driven animations** (`animation-timeline: view()`) — *subtle* reveals/parallax with zero JS; cross-browser baseline as of 2026. Use sparingly (gentle fade-in of sections at most).
- **Container queries** (`@container`, `cqi`) + `:has()` — components adapt to their space; ideal for the event-card list at various widths.
- **`text-wrap: balance`/`pretty`, `text-box: trim-both`** — quietly professional typography with no effort.
- **`interpolate-size: allow-keywords`** — animate `details`/accordion to `height: auto`; nice for a collapsed past-events archive.
- **View Transitions** — soft cross-page morphs instead of hard navigation; progressive enhancement, one meta/CSS opt-in.
- Typography pairing seen there worth remembering as a *category* (not to copy): an expressive variable serif (e.g. Fraunces) for display + a quiet mono/sans for body — display-serif-with-restraint suits a classical musician.
- Skip: WebGPU shaders, anchor-positioning zoos, spring-clipped blobs — showy, contra the brief.

## Phase 2: Stack & infrastructure (researched July 2026; decisions above)

### Site generator: keep Jekyll, but simplify it

- Jekyll is slow-moving but healthy enough (4.4.1, Jan 2025; GitHub Pages' legacy pipeline still depends on it, giving GitHub standing reason to keep it patched). For a tiny site, slow-moving is a feature: Liquid + front matter + Markdown haven't changed in a decade, no forced migrations. Ruby toolchain friction is already externalized (Actions builds; Docker for local preview).
- **The real maintenance surface is the vendored Minima 3.0 theme**, not Jekyll. Recommendation: do the redesign as **hand-rolled minimal templates** (one `default.html` layout, a nav include, one CSS file, a Liquid loop over events) — a few hundred fully-understood lines, nothing to ever upgrade. Redesign the *templates*, not the *platform*.
- Eleventy is the designated escape hatch if Jekyll ever dies (it speaks Liquid natively, so simplified templates port cheaply). Astro rejected: annual breaking-change cadence, app-oriented, overkill.

### Web authoring (so Marjorie can edit without git)

All git-backed CMSes store content as plain files in-repo — the CMS is a swappable veneer; the durable commitment is the one-file-per-event data model. Ranked:

1. **Sveltia CMS** — modern, phone-first editor; config-compatible with Decap (one-line fallback if its solo maintainer stops); needs one first-party free Cloudflare Worker for GitHub OAuth.
2. **Pages CMS** (hosted, pagescms.org) — zero infrastructure (GitHub App + one `.pages.yml`); free; depends on one person's hosted service. Cheap to try first.
3. **GitHub Issue Forms + Action** — max-durability floor: labeled form → Action commits the event file. Phone-friendly; editing existing entries is awkward.

Rejected: TinaCMS/Keystatic (Node/cloud mismatch), CloudCannon (~$55/mo), Prose.io (dead), raw GitHub YAML editing (build-breaking for non-technical editors). Prereq for any option: Marjorie needs a GitHub account with repo access (already on `_TODO.md`).

### DreamHost exit / domain cutover (checklist)

Verified July 2026: marjoriebagley.com is a stale WordPress site (newest post Aug 2015) on DreamHost shared hosting; DreamHost is also the **registrar** (expires 2027-03-18, auto-renew must stay on); nameservers DreamHost. With a custom domain, the GitHub project site serves at the domain root — the `/marjoriebagley` baseurl issue disappears automatically (Actions `configure-pages` handles it).

> ⚠️ **Before anything: MX records point to DreamHost — check whether any @marjoriebagley.com email address is in use.** "DNS Only" preserves email; full account closure would not.

1. Verify domain on GitHub (Settings → Pages → Add domain → TXT record `_github-pages-challenge-ibeatty`); keep TXT permanently (takeover protection).
2. DreamHost DNS: apex → A records 185.199.108/109/110/111.153; `www` → CNAME `ibeatty.github.io`. May need to set domain to "DNS Only" first. Don't delete MX if email matters.
3. Repo Settings → Pages → Custom domain → `marjoriebagley.com`.
4. Wait for Let's Encrypt cert; check Enforce HTTPS.
5. Archive anything wanted from the old WordPress site, then delete the DreamHost hosting plan choosing "No Hosting (DNS Only)" — registration survives.
6. Registration: stay at DreamHost registrar-only (~$16–20/yr, zero effort) or transfer to Cloudflare/Porkbun (~$10–12/yr, more steps). Not urgent either way.
7. Post-cutover: root loads, www/http redirect, internal links OK, email still flows.

## Open questions for Marjorie (content she must supply/decide)

1. Bio placeholders (`XX` ages/years) and final approval of bio.
2. Private-student policy: mention on the site or omit?
3. Studio-culture paragraph for the Studying page (her voice, what she looks for in students).
4. Whether a Listen/discography page is wanted, and which recordings/videos to feature.

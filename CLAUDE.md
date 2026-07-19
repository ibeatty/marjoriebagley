# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Jekyll static site — a professional website for violinist Marjorie Bagley (Professor of Violin at UNCG, Concertmaster of the Greensboro Symphony Orchestra). Ian Beatty (her husband) maintains it on her behalf. It builds and deploys to GitHub Pages via GitHub Actions. Live at https://ibeatty.github.io/marjoriebagley/.

**See `_RedesignPlan.md`** for the active redesign plan: content model, IA, stack/CMS research findings, and the DreamHost-exit checklist. **`_DesignResearch.md`** holds the comparable-musician survey (conventions, staleness traps, the five design directions). **`mockups/`** contains five self-contained homepage mockups for Marjorie's review — open `mockups/index.html` in a browser. **`_SetupSveltia.md`** has Ian's remaining manual CMS-auth steps.

## Project context & current goals

- **This is a rebuild** meant to replace Marjorie's older, stale site, **which is still the live public site.** This version is not yet the one the public sees.
- **The project stalled** and is now being picked up again. It was waiting on Marjorie to approve the design and to supply page content Ian can't write for her. Some pages are therefore still incomplete/placeholder, and that's expected.
- Tone to preserve: **low-key and professional.** Design improvements should feel *a little* more creative but stay understated — not flashy, not "because I can."
- **The events calendar is very out of date** and is a priority to refresh.

Two workstreams are active this phase (they interact — stack choice affects how designs get implemented):

1. **Visual design** — make it modestly more creative while keeping the low-key feel. Plan: generate **4–6 distinct design candidates** for Marjorie to choose among, informed by web research into what comparable musicians do (research for awareness, not imitation — "following the crowd" is explicitly not a value here).
2. **Infrastructure / maintainability** — the current update workflow (spin up the local Docker dev server, then push to GitHub) is used infrequently enough that the steps are hard to remember. Goals: make updates easier to perform, make **authoring new event entries** simple, and possibly **scrape-and-import human-designated concerts** from the Greensboro Symphony Orchestra site (the GSO listings don't make it obvious which concerts Marjorie is actually involved in, so selection must stay human-driven — see `scripts/scrape_gso_concerts.py`).

Additional constraints and aspirations:

- **Web-based form authoring is highly desirable** — ideally simple enough that **Marjorie can add/edit content herself** without touching git. Ian has avoided this so far only to keep the stack simple and GitHub Pages-friendly; a solution that stays static/free (e.g., a git-backed CMS) would square that circle.
- **Hosting must stay free/static (GitHub Pages).** A core objective of the redesign is to **stop paying for DreamHost hosting**, where the old site lives. No solution may reintroduce a paid server or database.
- **Minimize ongoing time/attention.** Ian and Marjorie are busy (three kids); nothing on the site may require much recurring effort to keep fresh. Concretely: **no design elements that depend on regularly refreshed content** — e.g., avoid photography-centric designs that look stale without new photos.
- **Low learning curve, durable tools.** Ian has decades of CMS experience but wants *simple* here. Avoid idiosyncratic/niche tools that demand updates, forward migrations, or rescue migrations if abandoned. Prefer boring, widely-adopted, long-lived technology. This weighs heavily in stack/CMS choice: project longevity and maintainer health matter as much as features.
- **Positioning — Marjorie's niche is an unusual hybrid**, and the site design must serve it: she is (a) a high-profile university faculty member whose studio depends on **active recruiting of 1:1 violin performance students**, and (b) a working performer (GSO concertmaster + ad-hoc chamber groups). She is **not** a private teacher (rare special cases aside), and she is neither "pure faculty" nor "pure performer" — the site should present the two roles as synergistic, and speak to both prospective students and concert audiences.

## Ground rules for future changes (read before "improving" anything)

This stack is deliberately small and boring; its entire value is that it
needs no attention. When in doubt, do less. The project's biggest risk is a
well-meaning change that adds maintenance surface or staleness.

**Invariants — do not violate without Ian's explicit sign-off:**

- No build tooling beyond Jekyll. No Sass/PostCSS/npm/bundlers/frameworks/
  theme gems — ever again. Styles remain exactly ONE plain-CSS file;
  recoloring means editing the token block at the top of it, nothing else.
- The public site currently ships zero JavaScript. Keep it that way absent a
  strong, Ian-approved reason.
- Never add: a blog/news section, any widget that can render an empty state
  (evergreen prose fallbacks instead — the reasons are in
  `_DesignResearch.md`), a photography-dependent design element, per-project
  nav items, or a nav beyond ~5 items.
- The `_events/` front-matter schema, `admin/config.yml` (Sveltia), and
  `scripts/scrape_gso_concerts.py` describe the same data — a field change in
  one MUST be mirrored in the other two in the same commit.
- `collections.events.output: false` stays false (no per-event pages).
- The auth worker (separate private repo `ibeatty/sveltia-cms-auth`) is
  configured via its `wrangler.toml` `[vars]` ONLY. Never set its plaintext
  vars in the Cloudflare dashboard — `wrangler deploy` wipes those on every
  git-triggered build.
- Don't delete `mockups/` until the design decision is final (it's Marjorie's
  review set); delete it at launch.

**Facts that will save you an afternoon:**

- The staging site's real URL is **https://ianbeatty.com/marjoriebagley/** —
  Ian's user-site custom domain fronts all his project sites, and
  `ibeatty.github.io/...` merely redirects there. Sveltia reports
  `ianbeatty.com` to the auth worker; the allowlist already covers it (and
  `marjoriebagley.com` for the future cutover).
- Auth worker health probe uses `site_id=` (NOT `domain=` — that always
  fails): `curl -sI ".../auth?provider=github&site_id=ianbeatty.com"` should
  return a `location: github.com/login/oauth/authorize...` header.
- Pushing to `main` deploys staging immediately. That is low-stakes today;
  **after the marjoriebagley.com DNS cutover the same push is the live
  public site** — recalibrate accordingly.
- `make build` completes with ZERO warnings. Any new warning is a regression
  you introduced.
- An event counts as "upcoming" through the end of its concert day
  (`_includes/event-split.html`); the Monday cron rebuild ages events out
  between pushes. If upcoming looks stale, check the cron ran.

**Recipes for the common tasks:**

- *Add a concert:* `make scrape` → `make scrape ARGS="--import N,M"` →
  review (set `role: Soloist` if deserved, trim blurb) → commit. Or let
  Marjorie do it in Sveltia at `/admin/`.
- *Recolor the site:* edit the ~9 custom properties at the top of
  `assets/css/main.css`. Touch nothing else.
- *Add a page:* new `.md` with `layout: page`, `title`, short `nav_title`,
  `permalink`; add to `header_pages` in `_config.yml` AND to the pages
  section of `admin/config.yml`.
- *Verify any change:* `make build`, then actually look at the affected
  pages (desktop AND ~375px mobile width) before pushing.

**Working with Ian:** verify claims against the live system before asserting
them; state uncertainty plainly (e.g., the violin's "1703" date is
unverified — never let it onto the public site as fact until Marjorie
confirms); never fabricate content (press quotes, dates, venues); prefer
small reversible commits with clear messages; keep `_TODO.md` and the
underscore docs in sync with reality as you work.

## Build & serve

Use the Makefile (run `make` for the list):

```bash
make serve   # local preview at http://localhost:4000, rebuilds on save
make build   # one-shot build into _site/
make setup   # one-time per machine: Homebrew Ruby + vendored gems
make scrape  # list upcoming GSO concerts (see Adding concerts below)
```

Local builds use Homebrew Ruby (`/opt/homebrew/opt/ruby/bin`) with gems
vendored into `vendor/bundle` (gitignored). Docker is NOT installed on this
machine — the old `docker run … bretfisher/jekyll-serve` workflow in
`_MaintenanceChecklist.md` is historical.

Deployment is automatic: pushing to `main` triggers `.github/workflows/jekyll.yml`, which builds with Jekyll 4.x on Ruby 3.2 and publishes to Pages. A weekly cron in the same workflow rebuilds Mondays 08:17 UTC so past events age out of the upcoming list without a push. There is no separate deploy step.

## Architecture & conventions

- **Templates are hand-rolled** (July 2026; the vendored Minima theme was deleted — no theme gem, no Sass). The whole surface is: `_layouts/default.html` (document shell, header/nav/footer), `home.html` (hero + role cards + season strip), `page.html` (interior; `wide: true` front matter opts out of the narrow column), plus `_includes/event-split.html`, `event-list.html`, `season-archive.html`. The layout implements the "Conservatory Modern" mockup direction (mockups/3-…), pending Marjorie's color verdict.
- **Styles are ONE plain-CSS file**: `assets/css/main.css`. No preprocessor, zero build warnings. **The entire palette is a token block at the top of that file** — recoloring the site (expected once Marjorie chooses) means editing ~9 custom properties and nothing else. Fonts (Libre Franklin + Source Serif 4, variable woff2, latin subset) are **self-hosted** in `assets/fonts/` — no third-party font requests; re-download via Google Fonts if ever changing families.
- **Nav** is generated from `header_pages` in `_config.yml`; a page's `nav_title` front matter (e.g. "Bio", "Season") overrides its `title` in the nav. Footer socials live under `socials:` in `_config.yml`. Footer year is Liquid (`site.time`), kept honest by the weekly cron rebuild.
- **Pages** are the markdown files listed in `header_pages` (`index.md`, `bio.md`, `studying.md`, `events.md`). The home hero headline/roles/cards are design furniture hard-coded in `_layouts/home.html`; the editable intro paragraph is `index.md`'s body. `/events/` groups past concerts by season (Aug–Jul, via `season-archive.html`).
- **Concerts are an `_events/` collection** (NOT blog posts; `_posts/` was deleted). One file per event, named `YYYY-MM-DD-slug.md`, front matter: `title`, `date` (concert date), `series` (`GSO Masterworks` / `GSO Pops` / `GSO Chamber` / `GSO` / `Chamber music` / `UNCG` / `Other`), optional `role` (e.g. `Soloist`), optional `venue`, optional `url`; body is an optional short blurb. `_includes/event-split.html` computes `upcoming`/`past` arrays at build time (an event stays upcoming through the end of its concert day); `_includes/event-list.html` renders them. Home shows upcoming (falling back to evergreen prose, NEVER an empty-state message — see `_DesignResearch.md` on why); `/events/` shows upcoming + past.
- **Web editing (Sveltia CMS)** lives at `/admin/` (`admin/index.html` + `admin/config.yml`, Decap-config-compatible). Remaining one-time auth setup for Ian is in `_SetupSveltia.md`; `base_url` in `admin/config.yml` is a placeholder until the Cloudflare auth worker is deployed. Schema changes to `_events/` front matter must be mirrored in `admin/config.yml`.

## Adding concerts

`scripts/scrape_gso_concerts.py` (via `make scrape` or `uv run`) lists upcoming GSO concerts from the site's Events Calendar REST API and imports only human-chosen ones (`--import 1,3` / `--import all`) as `_events/` files — Marjorie isn't in every GSO event, so selection is deliberately manual. Blurbs are auto-extracted from event pages best-effort. After importing: set `role: Soloist` where deserved, trim blurbs, commit. Details and known site quirks (WAF needs a browser User-Agent; sponsor-prefixed category names): `scripts/README.md`.

## Project notes

- `_TODO.md`, `_MaintenanceChecklist.md`, and `_SETUP_NOTES.md` are underscore-prefixed so Jekyll ignores them in the build; they track outstanding work and upkeep. Consult `_MaintenanceChecklist.md` before dependency/theme upgrades.
- `_config.yml` changes require a build restart to take effect locally.
- `Gemfile.lock` and `_site/` are gitignored.

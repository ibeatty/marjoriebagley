# Maintenance Checklist

*Rewritten Aug 29, 2026, to match the current stack (see `CLAUDE.md` for the
full architecture). The Minima/Sass/Docker-era version of this doc described
infrastructure that no longer exists; git history has it if you ever need it.*

## Every few months

- [ ] **Check GitHub Actions** — visit the [Actions tab](https://github.com/ibeatty/marjoriebagley/actions)
  and confirm recent deploys (including the weekly Monday cron rebuild) are
  green. A red run usually means an upstream dependency shifted; the error
  log is normally enough to diagnose.
- [ ] **Look at the live site** — https://ianbeatty.com/marjoriebagley/
  (or the eventual marjoriebagley.com after the DreamHost cutover). Desktop
  and phone width both; check `/admin/` still loads to a sign-in screen.
- [ ] **Skim Sveltia CMS's release notes** — https://github.com/sveltia/sveltia-cms/releases.
  It's pre-1.0 and updates almost daily; the admin panel is loaded unpinned
  (`admin/index.html`) so it always tracks latest, which is Sveltia's own
  recommended practice, but a config-schema change is possible. If `/admin/`
  ever shows a config error, the message names the exact field to fix (this
  happened once already — a widget type was renamed; see git log for
  `admin/config.yml`).

## Annually (or when something looks off)

- [ ] **Check Ruby's EOL status** — https://endoflife.date/ruby. The CI
  workflow (`.github/workflows/jekyll.yml`) pins a specific version; bump it
  before that version goes EOL, not after (a past-EOL Ruby was found and
  fixed Aug 2026 — it had quietly gone unsupported five months earlier).
  Match the local Homebrew Ruby version too, so CI and local dev don't drift.
- [ ] **Check Jekyll's changelog** — https://jekyllrb.com/news/. The Gemfile
  pins `~> 4.3`, which floats up through the 4.x line automatically; only a
  5.x release (not yet scheduled) would need a deliberate, tested migration.
- [ ] **Check the pinned GitHub Actions** — `actions/checkout`,
  `actions/configure-pages`, `actions/upload-pages-artifact`,
  `actions/deploy-pages` in the workflow file. Look at each one's releases
  page for its current major version; bumping is usually safe for a simple
  build-and-deploy workflow like this one, but skim the release notes first.
  (`ruby/setup-ruby` is intentionally left at `@v1` — the maintainers
  document that as a permanent floating tag, not a version to bump.)

## One-time recommendation, not yet done

- [ ] **Enable Dependabot** — currently disabled for this repo (confirmed
  Aug 2026). Repo Settings → Security → Dependabot → enable for GitHub
  Actions (and Bundler, for the Gemfile). Free, and would have caught the
  Ruby EOL issue automatically.

## If the build fails

1. Check the Actions tab's error log — it's almost always specific enough to
   act on directly.
2. Reproduce locally: `make build` (see `CLAUDE.md` for the dev workflow).
3. Check what actually changed — a content edit, a dependency bump, or an
   upstream shift (Sveltia, a GitHub Actions runner image, GSO's own site
   for the scraper).

## Key files

- `_config.yml` — Jekyll configuration
- `Gemfile` — Ruby gem versions
- `.github/workflows/jekyll.yml` — build + deploy + weekly cron
- `assets/css/main.css` — all styles; the palette token block is at the top
- `admin/config.yml` — Sveltia CMS schema (must stay in sync with `_events/`
  front matter and any page's `nav_title`/`permalink` — a rename that misses
  this file is a real bug that happened once already)
- `CLAUDE.md` — the canonical description of how everything fits together

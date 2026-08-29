# To-Do List

*(Restructured July 2026 during the redesign push. See `_RedesignPlan.md` for
the full plan and `_SetupSveltia.md` for CMS setup steps.)*

## Ian — infrastructure (one-time manual steps)

- [x] Sveltia CMS auth: DONE (Jul 19 2026) — worker live at
      sveltia-cms-auth.ian-8b3.workers.dev, config-as-code in its
      wrangler.toml, sign-in verified from ianbeatty.com/marjoriebagley/admin/
- [ ] Create GitHub account for M & invite as repo collaborator
- [ ] Pick which 2026–27 GSO concerts M is playing and import them:
      `make scrape`, then `make scrape ARGS="--import …"` (incl. Dragon's
      Chamber dates — the chamber series is covered now)
- [ ] Later, after design launch: DreamHost exit / domain cutover
      (checklist in `_RedesignPlan.md`; hosting is safe to drop — no email
      on the domain)

## Design

- [x] Implement hand-rolled templates (Conservatory Modern layout — Ian's
      decision, Jul 19 2026; replaced vendored Minima + Sass entirely; mobile
      looks good — supersedes old "improve appearance on phones" item). This
      is the live site today; it is a real baseline, not a placeholder.
- [ ] Show Marjorie the mockups (`mockups/index.html`, twelve directions —
      the layout is already decided, this is about the COLOR scheme) and get
      her verdict. Ian's first-look favorite among the palettes was #5
      Piedmont Dusk; #1/#2/#4 are close variations on one warm-paper-serif
      theme, #6 Nocturne/#7 Folio/#8 Overture were added to broaden the net.
- [ ] Verify the violin's year (caption in mockup 5b says 1703, per Ian's
      recollection) with Marjorie before it goes on the live site
- [ ] Recolor per Marjorie's verdict: edit the token block at the top of
      `assets/css/main.css` (~9 custom properties; nothing else changes)
- [ ] After launch decision: delete the `mockups/` directory

## Content (needs Marjorie)

- [ ] Update M's bio — fill the `XX` placeholders in `bio.md`, approve text
- [ ] Decide the private-student question flagged in red in `studying.md`
- [ ] Polish home page intro blurb (draft exists in `index.md`)
- [ ] Optional: pick recordings/videos for a "Listen" page (see
      `_RedesignPlan.md`)

## Done (maintenance pass, Aug 29 2026)

- [x] Bumped Ruby 3.2 (past EOL since Mar 2026) → 4.0 in CI, matching local
      dev; bumped the four stale GitHub Actions to current majors
      (checkout v7, configure-pages v6, upload-pages-artifact v5,
      deploy-pages v5); verified with a live CI run before calling it done
- [x] Fixed a real Sveltia config bug: hidden `nav_title`/`permalink`
      defaults for the Teaching page still pointed at the pre-rename
      `/studying/` — the next CMS edit would have silently reverted it
- [x] Fixed two genuinely broken `/events/` links missed by the
      studying→teaching/events→performances rename (404 page, and the
      home page's season-strip footer link — the latter was live on the
      homepage the whole time, since the evergreen-fallback branch is what
      renders whenever there's no upcoming event)
- [x] Deleted leftover Minima/Docker-era cruft: `_README.md`,
      `_SETUP_NOTES.md`, `script/*` (Bret Fisher jekyll-serve scaffold,
      fully superseded by the Makefile), `readme_banner.svg`, orphaned PWA
      manifest files never linked from any page, a tracked `.DS_Store`, and
      the now-dead `_config.yml` exclude entries pointing at them
- [x] Rewrote `_MaintenanceChecklist.md` to drop the now-irrelevant
      Docker/Minima checklist items and reflect the actual stack
- [x] Confirmed the weekly cron rebuild has run cleanly every Monday since
      launch with zero gaps — the unattended-maintenance design goal is
      holding up in practice

## Done (redesign push, July 2026)

- [x] Concerts restructured as `_events/` collection with automatic
      upcoming/past split + weekly rebuild
- [x] 2016 demo posts deleted; 2024–26 concerts migrated
- [x] Sveltia CMS wired at `/admin/`, auth completed and verified
      end-to-end (Jul 19 2026) — worker live at
      sveltia-cms-auth.ian-8b3.workers.dev, config-as-code in its
      wrangler.toml
- [x] GSO scraper rewritten on the Events Calendar REST API with
      human-choice import
- [x] `make serve` / `make build` dev wrapper (Homebrew Ruby; Docker no
      longer assumed)
- [x] Design research: 14 comparable musicians' sites surveyed
      (`_DesignResearch.md`)
- [x] Twelve design mockups produced (`mockups/`) — five from the initial
      research plus seven added widening the net per Ian's feedback
- [x] Studying/Events pages renamed to Teaching/Performances (permalink +
      nav label; filenames `studying.md`/`events.md` unchanged)

## Done (earlier)

- [x] Fixed Jekyll deprecation warnings (Minima 3.0, modern Sass color functions)
- [x] GitHub Pages build via GitHub Actions

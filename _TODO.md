# To-Do List

*(Restructured July 2026 during the redesign push. See `_RedesignPlan.md` for
the full plan and `_SetupSveltia.md` for CMS setup steps.)*

## Ian — infrastructure (one-time manual steps)

- [ ] Sveltia CMS auth: GitHub OAuth app + Cloudflare worker + fill in
      `base_url` in `admin/config.yml` (walkthrough: `_SetupSveltia.md`)
- [ ] Create GitHub account for M & invite as repo collaborator
- [ ] Pick which 2026–27 GSO concerts M is playing and import them:
      `make scrape`, then `make scrape ARGS="--import …"` (incl. Dragon's
      Chamber dates — the chamber series is covered now)
- [ ] Later, after design launch: DreamHost exit / domain cutover
      (checklist in `_RedesignPlan.md`; hosting is safe to drop — no email
      on the domain)

## Design

- [ ] Show Marjorie the mockups (`mockups/index.html`) and pick a direction
      (or a mix). Ian's first impressions (Jul 2026): #5 Piedmont Dusk has the
      most immediate positive impact (→ variant 5b adds the 1703 violin photo);
      #1/#2/#4 cluster too closely → wider-net additions #6 Nocturne,
      #7 Folio, #8 Overture
- [ ] Verify the violin's year (caption in 5b says 1703, per Ian's
      recollection) with Marjorie before launch
- [ ] Implement chosen design as hand-rolled templates (replaces vendored
      Minima; includes mobile appearance — supersedes old "improve appearance
      on phones" item)

## Content (needs Marjorie)

- [ ] Update M's bio — fill the `XX` placeholders in `bio.md`, approve text
- [ ] Decide the private-student question flagged in red in `studying.md`
- [ ] Polish home page intro blurb (draft exists in `index.md`)
- [ ] Optional: pick recordings/videos for a "Listen" page (see
      `_RedesignPlan.md`)

## Done (this push, July 2026)

- [x] Concerts restructured as `_events/` collection with automatic
      upcoming/past split + weekly rebuild
- [x] 2016 demo posts deleted; 2024–26 concerts migrated
- [x] Sveltia CMS wired at `/admin/` (pending auth steps above)
- [x] GSO scraper rewritten on the Events Calendar REST API with
      human-choice import
- [x] `make serve` / `make build` dev wrapper (Homebrew Ruby; Docker no
      longer assumed)
- [x] Design research: 14 comparable musicians' sites surveyed
      (`_DesignResearch.md`)
- [x] Five design mockups produced (`mockups/`)

## Done (earlier)

- [x] Fixed Jekyll deprecation warnings (Minima 3.0, modern Sass color functions)
- [x] GitHub Pages build via GitHub Actions

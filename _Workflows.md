# Workflows

*The single reference for "how do I do X" on this site. Written for Ian —
these tasks are infrequent enough to forget between visits. For the site's
architecture and the reasoning behind things, see `CLAUDE.md`.*

## Preview changes locally

```bash
make serve
```

Opens at `http://localhost:4000`. It watches the whole tree and rebuilds on
save — including new files, so you don't need to restart it after `make
scrape --import` adds an `_events/` file. Ctrl-C to stop.

One-shot build with no server (just to confirm nothing's broken):

```bash
make build
```

## Add a concert from the GSO's site

```bash
make scrape                          # numbered list of upcoming GSO concerts
make scrape ARGS="--import 1,3,5"    # import the ones Marjorie is playing
```

Flags must go inside `ARGS="..."` — `make scrape --import all` fails, because
`make` tries to parse `--import` as its own option, not the script's.
(Running the script directly instead of through `make` doesn't have this
problem: `uv run scripts/scrape_gso_concerts.py --import 1,3,5` works as
typed. Either way works equally well — `make scrape` is just shorter to
remember.)

Selection is manual because the GSO's own listing doesn't say which concerts
Marjorie is actually in.

After importing, review each new file in `_events/`:
- Set `role: Soloist` (or another role) if she's featured, not just playing
  concertmaster — the scraper can't know this.
- Trim or rewrite the auto-extracted blurb.
- Check `make serve` shows it correctly on the home page and `/performances/`.

Then commit and push — staging deploys automatically. Full detail on the
scraper itself: `scripts/README.md`.

## Add a concert or event by hand

For anything not on the GSO's site — a UNCG faculty recital, a chamber date —
either:

- **In Sveltia** (`/admin/`, works from a phone): "Concerts & Events" →
  add new entry, fill the form.
- **By hand:** new file in `_events/`, named `YYYY-MM-DD-slug.md`:
  ```yaml
  ---
  title: "Concert Title"
  date: 2027-03-15
  series: UNCG            # GSO Masterworks | GSO Pops | GSO Chamber | GSO | Chamber music | UNCG | Other
  role: Soloist            # optional — omit for ordinary concertmaster duty
  venue: Tanger Center, Greensboro NC   # optional
  url: https://example.com/tickets      # optional
  ---
  Optional short blurb about the program.
  ```
  Preview with `make serve`, then commit and push.

## Edit page text (Bio, Teaching, Home intro)

Two equivalent paths:

- **In Sveltia** (`/admin/`, works from a phone) — "Site Pages" → pick the
  page, edit, save. Commits directly under your GitHub account.
- **By hand** — edit the `.md` file (`bio.md`, `studying.md`, `index.md`),
  check it with `make serve`, then commit and push.

The home page's big hero text (headline, the Teach/Lead/Play lines, the three
role cards) isn't in any `.md` file — it's hard-coded in `_layouts/home.html`,
since it's page furniture rather than prose. Edit that file directly for
those.

## Recolor the site

Edit the ~9 custom properties in the `:root` token block at the very top of
`assets/css/main.css`. Nothing else needs to change. Preview with `make
serve` before committing — the whole point of the token block is that a
recolor is exactly this contained.

## Add a new page

1. New `.md` file with front matter: `layout: page`, `title`, a short
   `nav_title` (shown in the nav instead of the full title), `permalink`.
2. Add the filename to `header_pages` in `_config.yml`.
3. Add an entry for it in the `pages` section of `admin/config.yml`, so it's
   editable in Sveltia too (see the existing `bio`/`studying` entries as a
   template — same schema, different `file:`/`permalink` default).
4. `make build` and check it before pushing.

## Check whether a deploy succeeded

- Browser: https://github.com/ibeatty/marjoriebagley/actions
- CLI: `gh run list --repo ibeatty/marjoriebagley --limit 5`

A push to `main` deploys within a couple of minutes. There's also a
scheduled run every Monday (see "the weekly cron job" in `CLAUDE.md`) that
deploys even with no code changes, so the events list stays current.

## Switch which GitHub account `gh`/git acts as

If a push fails with a permissions error, `gh` may have a different account
active than the one with write access to this repo:

```bash
gh auth status                                    # see which account is active
gh auth switch --hostname github.com --user ibeatty
```

## Give Marjorie access to the CMS

One-time, once she has a GitHub account: repo → **Settings → Collaborators**
→ add her with write access. She then signs in at `/admin/` the same way you
do; her edits commit under her own name. Full CMS auth setup (already done,
kept for reference): `_SetupSveltia.md`.

## Set up a new machine

```bash
make setup     # installs Homebrew Ruby + project gems
```

If you've already run this before and just updated the Gemfile or your Ruby
version: `make update-gems`.

## Periodic maintenance

Not a task list to run through now — see `_MaintenanceChecklist.md` for the
recurring checks (dependency freshness, GitHub Actions versions, Dependabot).

## Eventually: point marjoriebagley.com at this site

A future one-time task, not a recurring one — see the DreamHost-exit
checklist in `_RedesignPlan.md`.

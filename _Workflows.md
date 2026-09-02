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
- Don't want one after all (wrong concert, `--import all` grabbed too much)?
  Just delete its file — see "Undo something before it's pushed" below.

Then commit and push — staging deploys automatically. Full detail on the
scraper itself: `scripts/README.md`.

Want Marjorie to look over a batch before it goes out, instead of pushing
straight to `main`? See the next section.

## Preview a batch of changes with Marjorie before publishing

*One-time setup required first — `_SetupCloudflarePreview.md`. Currently
optional/opt-in, used mainly for concert-import batches; becomes the
required flow for everything after the `marjoriebagley.com` cutover (see
`_RedesignPlan.md`).*

A separate branch, `preview`, deploys automatically to its own stable
Cloudflare Pages URL — independent of the real site, which only ever
reads `main`. A GitHub Actions workflow
(`.github/workflows/sync-preview.yml`) keeps `preview` merged up to date
with `main` automatically on every push to `main` — including a future
Sveltia save, which nobody would otherwise remember to sync — so it can
only ever be equal to or ahead of the live site, never behind. You don't
need to sync it by hand, though `git checkout preview && git merge main`
still works if you want it caught up immediately rather than waiting the
minute or so for the Action to run. The loop:

1. `git checkout preview`.
2. Make this round's changes there instead of on `main`.
   (Scraping: `make scrape ARGS="--import 1,3"` writes the files the same
   way regardless of which branch is checked out.)
3. `git push` — the preview URL updates within about a minute.
4. Send Marjorie the preview URL (same one every time — bookmark it).
   She looks it over on her own time, no git/localhost/anything involved
   on her end, and tells you what to add, fix, or drop.
5. Make those changes on `preview`, push again, repeat until she's happy.
6. **Publish:** merge `preview` into `main` on github.com — open a pull
   request (`github.com/ibeatty/marjoriebagley/compare/main...preview`,
   or `gh pr create --base main --head preview`) and merge it, or simply
   `git checkout main && git merge preview && git push` if you don't need
   the PR's diff view first. Either way, this is the one step you execute
   — Marjorie just needs to say "publish it."
7. After merging, `preview` and `main` are identical again — no need to
   delete or recreate the branch; the next round starts from step 1.

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

## Edit or delete a concert that's already published

Once an event is live, how it was originally created — scraped, hand-added,
or entered in Sveltia — doesn't matter. It's just a file in `_events/` in the
repo, and either path always works:

- **In Sveltia** (`/admin/`) — open it under "Concerts & Events," edit or
  delete, save. No git required.
- **By hand** — edit or `git rm` the file, commit, push.

Sveltia's save skips the local git steps, but the site still takes the same
~1–2 minute build-and-deploy as any other push before the change is actually
live — it isn't instant, just more convenient.

## Undo something before it's pushed

Nothing you do locally reaches the live site until you `git push` — `make
scrape --import`, hand-adding a file, and editing an existing page are all
just changes sitting in your working directory until then. So before you
push:

- **Delete a file you don't want** (a bad import, a hand-added event you
  changed your mind about): `git status` shows it as untracked (`??`) — just
  `rm _events/that-file.md`. It's as if it never existed; no trace, nothing
  to clean up in git history.
- **Abandon an edit to an existing file** (e.g. you started tweaking `bio.md`
  and want to revert to what's already live): `git checkout -- bio.md`
  discards the change and restores the last-committed version.
- **Check what you're about to publish, all at once:** `git status` lists
  everything changed/added; `git diff` shows the actual line-by-line changes
  for anything already tracked.

This only applies pre-push — Sveltia has no equivalent local-only stage,
since it commits directly on save (see "Edit or delete a concert that's
already published" above). Once something is live, fixing it means a normal
follow-up edit, not an undo.

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

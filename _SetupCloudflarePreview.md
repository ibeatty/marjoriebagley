# Preview site on Cloudflare Pages: one-time setup (Ian)

**What this is:** a second, independent deployment of this same Jekyll site,
built automatically from the `preview` branch (not `main`), living at its own
Cloudflare Pages URL. It exists so a batch of changes — most often a round of
scraped concerts — can be reviewed by Marjorie at a stable link before you
merge them into `main`, where they become live on the real site. It never
touches the production GitHub Pages deployment; the two are entirely
separate systems reading two different branches of the same repo.

**Why Cloudflare Pages** rather than a second GitHub Pages site: GitHub
Pages only serves one branch per repo natively, with no built-in per-branch
preview URLs. Cloudflare Pages provides that as a standard, off-the-shelf
feature, and you already have a Cloudflare account from the Sveltia auth
worker — this is one more project on it, not a new relationship. See the
"hosting" note in `CLAUDE.md` for how this squares with the project's
GitHub-Pages-only rule for the *production* site (short version: it does,
because this is preview-only tooling, not where the public site lives).

## Steps (~15 minutes)

1. **Cloudflare dashboard → Workers & Pages → Create application → Pages
   tab → Connect to Git.** Select the `ibeatty/marjoriebagley` repository.
   (If Cloudflare hasn't been granted access to this specific repo before,
   it'll prompt you to add it — same GitHub App used for the auth worker.)

2. **Set up builds and deployments:**
   - **Production branch:** `preview` — yes, `preview`, not `main`. Within
     *this Cloudflare project*, "production branch" just means "the branch
     that deploys to the clean primary URL" — it has nothing to do with our
     repo's real `main`, which this Cloudflare project should never touch.
   - **Build command:** `bundle exec jekyll build`
   - **Build output directory:** `_site`
   - **Root directory:** leave as the default (repo root)

3. **Environment variables** (Settings → add before or after the first
   deploy): `RUBY_VERSION` = `4.0`, matching CI and local dev. If the build
   fails specifically at the Ruby install step (unlikely, but 4.0 is fairly
   new), try `3.4` instead — Cloudflare's build image installs whichever
   version you name on demand, it isn't a fixed list, but a brand-new major
   release is the one place that could plausibly lag.

4. **Stop this project from also building `main`.** Find the preview-branch
   deployment controls (Settings → Builds & deployments, look for "Preview
   branches" or "Branch control" — Cloudflare's own menu wording here has
   shifted between docs versions, so poke around that settings page if it's
   not exactly where described). Set it to **Custom branches**, and make
   sure `main` is excluded (leaving the include list empty, or excluding
   `*` and including nothing, both work). The only branch this Cloudflare
   project should ever build is `preview`.

5. **Deploy, then find the URL** on the project's Overview page — something
   like `https://<project-name>.pages.dev` (you'll pick `<project-name>`
   during setup; `marjoriebagley-preview` is a reasonable choice). That URL
   is permanent and always reflects the latest push to `preview` — bookmark
   it, it's what you'll send Marjorie.

6. **Verify:** open the URL. Since `preview` currently == `main`, it should
   look identical to the live site. Then test the real loop once: push a
   trivial change to `preview` locally (`git checkout preview`, edit
   something, `git push`) and confirm the Cloudflare URL updates within a
   minute or so.

## Using it (once set up)

See "Preview a batch of changes with Marjorie before publishing" in
`_Workflows.md` for the day-to-day flow. Short version: push to `preview`
instead of `main` when you want a review round; share the Cloudflare URL;
merge `preview` → `main` on github.com when Marjorie signs off.

## Not done yet, and intentionally so

`main` has no branch protection — routine edits can still go straight there,
exactly as before. This preview setup is opt-in per batch of changes, not a
mandatory gate, until the `marjoriebagley.com` cutover. See the DNS-cutover
checklist in `_RedesignPlan.md` for when that changes.

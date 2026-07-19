# Sveltia CMS: one-time setup steps (Ian)

The CMS itself is already wired up: `admin/index.html` + `admin/config.yml`
deploy with the site, so the editor lives at `<site-url>/admin/`. What remains
is the auth plumbing (≈20 minutes, once) so that GitHub sign-in works from the
browser, plus giving Marjorie access. Content is always plain files in the
repo — if Sveltia ever dies, swap the one script tag in `admin/index.html`
for Decap CMS and nothing else changes.

## 0. Try it without any setup (optional)

Sveltia has a local mode that needs no auth at all, good for a first look:

1. `make serve` and open <http://localhost:4000/admin/>
2. Click **Work with Local Repository** and select the repo folder.
3. Edits write directly to your working tree (commit them yourself).

(Chrome/Edge only — it uses the File System Access API.)

## 1. Create a GitHub OAuth App

GitHub → Settings → Developer settings → OAuth Apps → **New OAuth App**:

- **Application name:** `Marjorie Bagley site editor` (anything)
- **Homepage URL:** `https://ibeatty.github.io/marjoriebagley/`
- **Authorization callback URL:** `https://TEMPORARY.example/callback` — placeholder;
  you'll replace it with the Worker URL in step 3.

Save, then note the **Client ID** and generate a **Client secret** (keep the tab open).

## 2. Deploy the auth Worker on Cloudflare

The Worker is Sveltia's first-party OAuth proxy (free Cloudflare tier is plenty;
it only runs for a moment at sign-in).

1. Create a free Cloudflare account if you don't have one.
2. Go to <https://github.com/sveltia/sveltia-cms-auth> and click the
   **Deploy to Cloudflare Workers** button in the README; follow the flow
   (it copies the repo under your GitHub account and deploys). The form's
   prefilled defaults are all correct — Git account `ibeatty`, project name
   `sveltia-cms-auth`, empty build command, `pnpm run deploy` — and the
   "private repository" checkbox is cosmetic (secrets never live in that
   repo). Just click **Deploy**.
3. In the Worker's **Settings → Variables and Secrets**, add:
   - `GITHUB_CLIENT_ID` — from step 1
   - `GITHUB_CLIENT_SECRET` — from step 1 (type: Secret)
   - `ALLOWED_DOMAINS` — `ibeatty.github.io, marjoriebagley.com`

   ⚠️ Variables only take effect on the NEXT deploy — after saving them,
   hit the redeploy/Deploy button the Variables screen offers. ("I set the
   secrets but sign-in still fails" almost always means this was skipped.)
4. Note the Worker URL, e.g. `https://sveltia-cms-auth.<account>.workers.dev`
   (shown on the Worker's overview page). If the overview says **"No URLs
   enabled"**: Settings → Domains & Routes → enable the **workers.dev** route
   (registering the one-time account subdomain if prompted — the name is
   cosmetic). It can take a minute to start resolving after enabling.

### Worker health check (no browser needed)

```bash
curl -sI "https://sveltia-cms-auth.ian-8b3.workers.dev/auth?provider=github&site_id=ibeatty.github.io" | grep -i location
```

A `location: https://github.com/login/oauth/authorize?...` line means the
worker is fully configured. Note the parameter is **`site_id`** (a
Netlify-era convention Sveltia inherited) — probing with `domain=` always
returns UNSUPPORTED_DOMAIN and proves nothing.

Config lives as code now: `ALLOWED_DOMAINS` and `GITHUB_CLIENT_ID` are set
in the worker repo's `wrangler.toml` `[vars]` (plus `keep_vars = true`), so
every git-triggered build applies them; only `GITHUB_CLIENT_SECRET` lives as
a dashboard Secret (those survive deploys). Don't set the two plaintext vars
in the dashboard — `wrangler deploy` treats the toml as the source of truth.

## 3. Connect the pieces

1. Back in the GitHub OAuth App: set the real **callback URL** =
   `https://<worker-url>/callback`.
2. In `admin/config.yml`: replace the `base_url` placeholder with the Worker
   URL. Commit and push.

## 4. Test

Open `https://ibeatty.github.io/marjoriebagley/admin/`, click **Sign in with
GitHub**, authorize, and try editing an event. Saving commits to `main` and
triggers a deploy — check the Actions tab if the site doesn't update in ~2 min.

## 5. Give Marjorie access

1. Create her GitHub account (already on the to-do list).
2. Repo → Settings → Collaborators → invite her (write access).
3. She accepts the invite, then signs in at `/admin/` with her account.
   Her edits are committed under her own name.
4. Phone use works — Sveltia is mobile-friendly; she can bookmark `/admin/`
   on her home screen.

## After the marjoriebagley.com cutover

- `ALLOWED_DOMAINS` already includes the custom domain; no Worker change needed.
- Update `site_url`/`display_url` in `admin/config.yml` to the custom domain
  (cosmetic only).

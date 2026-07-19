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
   (it forks the repo and deploys).
3. In the Worker's **Settings → Variables**, add:
   - `GITHUB_CLIENT_ID` — from step 1
   - `GITHUB_CLIENT_SECRET` — from step 1 (encrypt/secret type)
   - `ALLOWED_DOMAINS` — `ibeatty.github.io, marjoriebagley.com`
4. Note the Worker URL, e.g. `https://sveltia-cms-auth.<account>.workers.dev`.

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

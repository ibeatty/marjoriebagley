# Site automation scripts

## scrape_gso_concerts.py

Lists upcoming Greensboro Symphony concerts and imports human-chosen ones as
event files in `_events/`. Marjorie isn't in every GSO event and the listings
don't say which, so selection is deliberately manual.

Requires [uv](https://docs.astral.sh/uv/) (dependencies are declared inline
in the script — nothing to install).

```bash
# From the repo root (or `make scrape`):
uv run scripts/scrape_gso_concerts.py                 # numbered list of upcoming concerts
uv run scripts/scrape_gso_concerts.py --import 1,3,5  # import those numbers
uv run scripts/scrape_gso_concerts.py --import all    # import every new one
uv run scripts/scrape_gso_concerts.py --start 2027-01-01  # look further ahead
```

Already-imported concerts show a `[have]` marker (matched by event URL) and
are never overwritten.

### How it works

Data comes from the GSO site's Events Calendar REST API
(`/wp-json/tribe/events/v1/events`) — a standard WordPress-plugin interface,
much more stable than scraping page HTML. Blurbs aren't included in the API,
so `--import` also fetches each chosen event's page and extracts the program
paragraphs (performers, repertoire) as the event body, best-effort.

Two quirks encoded in the script:

- The GSO's web application firewall rejects requests without a browser-like
  `User-Agent` (returns 406) — hence the header in the script.
- Category names are sponsor-prefixed ("Bank of Oak Ridge Masterworks");
  the script maps them onto our series values (`GSO Masterworks`, `GSO Pops`,
  `GSO Chamber`, `GSO`).

### After importing

Review each new file in `_events/` (or in the Sveltia editor at `/admin/`):

- Set `role: Soloist` if Marjorie is featured (the scraper can't know).
- Trim or rewrite the auto-extracted blurb.
- Then commit and push — the site deploys automatically.

### If it breaks

If the API stops responding, the GSO likely changed WordPress plugins or
their firewall rules. Check `https://greensborosymphony.org/wp-json/tribe/events/v1/events`
in a browser; adjust `API`/`HEADERS` in the script accordingly.

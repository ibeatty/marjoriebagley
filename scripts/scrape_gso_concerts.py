#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "requests>=2.31.0",
# ]
# ///
"""
List upcoming Greensboro Symphony concerts and import chosen ones as events.

Marjorie isn't in every GSO event (and the listings don't say), so importing
is deliberately human-driven: run with no arguments to see a numbered list,
then rerun with --import to create files in _events/ for the ones she's
playing. Review them afterwards (locally, or in the Sveltia editor at
/admin/) — especially to set `role: Soloist` where deserved and to trim the
auto-extracted blurb.

Usage (from the repo root, or via `make scrape`):
    uv run scripts/scrape_gso_concerts.py                 # list upcoming concerts
    uv run scripts/scrape_gso_concerts.py --import 1,3,5  # import those numbers
    uv run scripts/scrape_gso_concerts.py --import all    # import everything new
    uv run scripts/scrape_gso_concerts.py --start 2027-01-01   # look further out

Data comes from the site's Events Calendar REST API
(/wp-json/tribe/events/v1/events) — a stable WordPress-plugin interface, far
less likely to break than HTML scraping. Concert blurbs aren't in the API, so
--import additionally fetches each chosen event's page and extracts the
program/description paragraphs as the event body (best effort; edit after).
"""

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

import requests

BASE = "https://greensborosymphony.org"
API = f"{BASE}/wp-json/tribe/events/v1/events"
# The GSO's WAF rejects requests without a browser-like User-Agent.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    )
}

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_DIR = REPO_ROOT / "_events"

# Venue names as they should appear on the site (API name -> short form).
VENUE_MAP = {
    "Steven Tanger Center for the Performing Arts": "Tanger Center, Greensboro NC",
}


def series_for(categories):
    """Map GSO category names (often sponsor-prefixed) onto our series values."""
    joined = " ".join(c.get("name", "") for c in categories).lower()
    if "masterworks" in joined:
        return "GSO Masterworks"
    if "pops" in joined:
        return "GSO Pops"
    if "chamber" in joined:
        return "GSO Chamber"
    return "GSO"


def fetch_events(start):
    """Fetch all events from `start` onward, following API pagination."""
    events, page, total_pages = [], 1, 1
    while page <= total_pages:
        resp = requests.get(
            API,
            params={"start_date": start, "per_page": 50, "page": page},
            headers=HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        total_pages = data.get("total_pages", 1)
        for e in data.get("events", []):
            slug = e["url"].rstrip("/").rsplit("/", 1)[-1]
            venue = (e.get("venue") or {}).get("venue", "")
            events.append(
                {
                    "date": e["start_date"][:10],
                    "title": html.unescape(e["title"]).strip(),
                    "series": series_for(e.get("categories", [])),
                    "venue": VENUE_MAP.get(venue, venue),
                    "url": e["url"],
                    "slug": slug,
                }
            )
        page += 1
    events.sort(key=lambda e: e["date"])
    return events


def known_urls():
    """Event URLs already present in _events/ front matter."""
    urls = set()
    for f in EVENTS_DIR.glob("*.md"):
        m = re.search(r"^url:\s*(\S+)", f.read_text(encoding="utf-8"), re.M)
        if m:
            urls.add(m.group(1).rstrip("/"))
    return urls


def extract_blurb(event_url):
    """Best-effort: pull program/description paragraphs from the event page."""
    try:
        resp = requests.get(event_url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException:
        return ""
    page = resp.text
    blurb_paras = []
    for para in re.findall(r"<p[^>]*>(.*?)</p>", page, re.S):
        para = re.sub(r"<br\s*/?>", "\n", para)
        text = html.unescape(re.sub(r"<[^>]+>", "", para))
        # <br>-separated program lines would collapse in Markdown anyway;
        # join them with a middle dot, which reads well inline.
        text = " · ".join(
            line.strip() for line in text.splitlines() if line.strip()
        )
        # Skip navigation menus and boilerplate that WordPress wraps in <p>.
        if len(text) < 40 or "View All Concerts" in text:
            continue
        blurb_paras.append(text)
        if len(blurb_paras) == 2:
            break
    return "\n\n".join(blurb_paras)


def write_event(ev, blurb):
    lines = ["---"]
    lines.append(f'title: "{ev["title"]}"')
    lines.append(f"date: {ev['date']}")
    lines.append(f"series: {ev['series']}")
    if ev["venue"]:
        lines.append(f"venue: {ev['venue']}")
    lines.append(f"url: {ev['url']}")
    lines.append("---")
    body = (blurb + "\n") if blurb else ""
    dest = EVENTS_DIR / f"{ev['date']}-{ev['slug']}.md"
    dest.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--start", default=date.today().isoformat(),
                    help="earliest date to list (YYYY-MM-DD, default today)")
    ap.add_argument("--import", dest="imports", metavar="N,M|all",
                    help="import these list numbers ('all' = every new one)")
    args = ap.parse_args()

    print(f"Fetching GSO events from {args.start} on …")
    events = fetch_events(args.start)
    if not events:
        print("No events returned — check the site or try an earlier --start.")
        return 1

    have = known_urls()
    for e in events:
        e["have"] = e["url"].rstrip("/") in have

    width = max(len(e["title"]) for e in events)
    for i, e in enumerate(events, 1):
        mark = "have" if e["have"] else "    "
        print(f"{i:3}. [{mark}] {e['date']}  {e['title']:<{width}}  {e['series']}")

    if not args.imports:
        print("\nNothing imported. Rerun with --import N,M (or --import all) "
              "for the concerts Marjorie is playing.")
        return 0

    if args.imports.strip().lower() == "all":
        chosen = [e for e in events if not e["have"]]
    else:
        try:
            idxs = [int(n) for n in args.imports.replace(" ", "").split(",")]
        except ValueError:
            print(f"Couldn't parse --import '{args.imports}' — use e.g. 1,3,5 or all.")
            return 1
        bad = [n for n in idxs if not 1 <= n <= len(events)]
        if bad:
            print(f"Out-of-range number(s): {bad} (list has {len(events)} entries).")
            return 1
        chosen = [events[n - 1] for n in idxs]

    imported = 0
    for e in chosen:
        if e["have"]:
            print(f"skip (already have): {e['title']}")
            continue
        blurb = extract_blurb(e["url"])
        dest = write_event(e, blurb)
        imported += 1
        print(f"wrote {dest.relative_to(REPO_ROOT)}"
              + ("" if blurb else "   (no blurb found — add one by hand)"))

    if imported:
        print(f"\n{imported} event(s) imported. Review them (role/blurb/venue), "
              "then commit and push — or edit further in Sveltia at /admin/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

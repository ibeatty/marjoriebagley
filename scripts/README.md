# GSO Concert Scraper

This directory contains automation scripts for the Marjorie Bagley website.

## scrape_gso_concerts.py

Automatically scrapes concert information from the Greensboro Symphony Orchestra website and creates Jekyll post files.

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package installer (handles dependencies automatically)

### Usage

From the repository root directory:

```bash
uv run scripts/scrape_gso_concerts.py
```

Or make it executable and run directly:

```bash
chmod +x scripts/scrape_gso_concerts.py
./scripts/scrape_gso_concerts.py
```

No need to install dependencies separately - `uv` handles them automatically using inline script metadata!

The script will:
1. Fetch upcoming concerts from https://greensborosymphony.org/concerts/
2. Extract concert information (title, date, description, URL)
3. Create Jekyll post files in `_posts/` directory
4. Skip concerts that already have posts

### Post Format

Generated posts follow this format:

```markdown
---
layout: post
category: "GSO Masterworks"
title: "Concert Title"
---

Concert description here.

See [the GSO's event page](https://url) for details.
```

### Categories

The script automatically categorizes concerts:
- **GSO Masterworks** - Classical concerts (contains "masterworks")
- **GSO Pops** - Popular music concerts (contains "pops")
- **GSO Masterworks/Solo** - Concertos and solo performances
- **GSO** - Default for other concerts

### Troubleshooting

**No concerts found:**
The GSO website structure may have changed. To fix:

1. Open https://greensborosymphony.org/concerts/ in a browser
2. Inspect the HTML (right-click → Inspect)
3. Find the CSS selectors for concert elements
4. Update the `extract_concert_info()` function in the script with new selectors

**Date parsing errors:**
If concert dates can't be parsed, posts will use the current date. You may need to manually adjust the filename date.

**Duplicate posts:**
The script skips posts that already exist (based on filename). If you need to regenerate a post, delete the old one first.

### Manual Editing

After running the script, review the generated posts in `_posts/` and:
- Add more details from the GSO website
- Fix any date parsing issues
- Adjust categories if needed
- Add venue information if available

### Future Improvements

Potential enhancements:
- Add Playwright support for JavaScript-heavy pages
- Extract venue information
- Parse performer names
- Add concert series/season information
- Schedule automatic runs (cron/GitHub Actions)

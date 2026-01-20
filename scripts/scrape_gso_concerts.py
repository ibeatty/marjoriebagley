#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = [
#   "requests>=2.31.0",
#   "beautifulsoup4>=4.12.0",
# ]
# ///
"""
Scrape Greensboro Symphony Orchestra concerts and create Jekyll posts.

This script fetches concert information from the GSO website and generates
markdown files in the _posts directory for the Jekyll site.

Usage:
    uv run scripts/scrape_gso_concerts.py

Or simply:
    ./scripts/scrape_gso_concerts.py
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import sys

# Base URL for GSO website
GSO_BASE_URL = "https://greensborosymphony.org"
GSO_CONCERTS_URL = f"{GSO_BASE_URL}/concerts/"

def fetch_concerts():
    """Fetch the concerts page and parse it."""
    print(f"Fetching concerts from {GSO_CONCERTS_URL}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(GSO_CONCERTS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching concerts: {e}")
        sys.exit(1)

def extract_concert_info(soup):
    """Extract concert information from the parsed HTML."""
    concerts = []

    # Try to find concert listings - adjust selectors based on actual HTML structure
    # These are common patterns, but may need adjustment
    concert_elements = soup.select('.event, .concert-item, article, .tribe-events-list-event-row')

    if not concert_elements:
        print("Warning: No concert elements found with standard selectors.")
        print("The page structure may have changed. Manual inspection needed.")
        return concerts

    for element in concert_elements:
        concert = {}

        # Try various selectors for title
        title_elem = (element.select_one('h2, h3, .event-title, .tribe-events-list-event-title') or
                     element.select_one('a[href*="/event/"]'))
        if title_elem:
            concert['title'] = title_elem.get_text(strip=True)
            # Get event URL if available
            link = title_elem.find('a') if title_elem.name != 'a' else title_elem
            if link and link.get('href'):
                concert['url'] = link['href']
                if not concert['url'].startswith('http'):
                    concert['url'] = GSO_BASE_URL + concert['url']

        # Try to find date
        date_elem = element.select_one('.event-date, .tribe-event-date-start, time')
        if date_elem:
            concert['date_text'] = date_elem.get_text(strip=True)
            # Try to parse datetime attribute if available
            if date_elem.has_attr('datetime'):
                concert['datetime'] = date_elem['datetime']

        # Try to find description
        desc_elem = element.select_one('.event-description, .tribe-events-list-event-description, p')
        if desc_elem:
            concert['description'] = desc_elem.get_text(strip=True)

        # Try to find category/series
        category_elem = element.select_one('.event-category, .tribe-events-event-categories')
        if category_elem:
            concert['category'] = category_elem.get_text(strip=True)

        if concert.get('title'):  # Only add if we found at least a title
            concerts.append(concert)

    return concerts

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def parse_concert_date(concert):
    """Try to parse a date from the concert information."""
    # Try to parse from datetime attribute first
    if 'datetime' in concert:
        try:
            return datetime.fromisoformat(concert['datetime'].replace('Z', '+00:00'))
        except:
            pass

    # Try to parse from date text
    if 'date_text' in concert:
        date_text = concert['date_text']
        # Try common date formats
        for fmt in ['%B %d, %Y', '%b %d, %Y', '%m/%d/%Y', '%Y-%m-%d']:
            try:
                return datetime.strptime(date_text, fmt)
            except ValueError:
                continue

    # Default to current date if we can't parse
    print(f"Warning: Could not parse date for '{concert.get('title', 'Unknown')}', using current date")
    return datetime.now()

def create_post(concert, posts_dir):
    """Create a Jekyll post file from concert information."""
    # Parse date for filename
    concert_date = parse_concert_date(concert)
    date_str = concert_date.strftime('%Y-%m-%d')

    # Create slug from title
    slug = slugify(concert['title'])
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)

    # Check if post already exists
    if os.path.exists(filepath):
        print(f"  Skipping {filename} (already exists)")
        return False

    # Determine category
    title = concert['title'].lower()
    if 'masterworks' in title:
        category = 'GSO Masterworks'
    elif 'pops' in title:
        category = 'GSO Pops'
    elif 'solo' in title or 'concerto' in title:
        category = 'GSO Masterworks/Solo'
    else:
        category = concert.get('category', 'GSO')

    # Create post content
    content = f"""---
layout: post
category: "{category}"
title: "{concert['title']}"
---

"""

    # Add description if available
    if 'description' in concert:
        content += f"{concert['description']}\n\n"

    # Add link to event page
    if 'url' in concert:
        content += f"See [the GSO's event page]({concert['url']}) for details.\n"

    # Write the file
    with open(filepath, 'w') as f:
        f.write(content)

    print(f"  Created {filename}")
    return True

def main():
    """Main function to scrape concerts and create posts."""
    # Determine posts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    posts_dir = os.path.join(repo_dir, '_posts')

    if not os.path.exists(posts_dir):
        print(f"Error: _posts directory not found at {posts_dir}")
        sys.exit(1)

    print("=" * 60)
    print("GSO Concert Scraper")
    print("=" * 60)

    # Fetch and parse concerts
    soup = fetch_concerts()
    concerts = extract_concert_info(soup)

    if not concerts:
        print("\nNo concerts found!")
        print("\nThe website structure may have changed.")
        print("Please open the GSO concerts page in a browser and inspect")
        print("the HTML to update the selectors in this script.")
        sys.exit(1)

    print(f"\nFound {len(concerts)} concerts")
    print("-" * 60)

    # Create posts
    created_count = 0
    for concert in concerts:
        if create_post(concert, posts_dir):
            created_count += 1

    print("-" * 60)
    print(f"\nSummary: Created {created_count} new posts")
    print("=" * 60)

if __name__ == '__main__':
    main()

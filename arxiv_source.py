"""Fetch recent papers from arXiv that match our keywords.

Run this file on its own to test it:  python arxiv_source.py
"""
import urllib.parse

import feedparser
import requests

ARXIV_API = "https://export.arxiv.org/api/query"


def build_query(keywords):
    """Turn ["protein design", "macrocycle"] into an arXiv search string.

    arXiv's search syntax: ti:"..." searches titles, abs:"..." searches abstracts.
    Quotes keep multi-word phrases together. OR means any match counts.
    """
    parts = []
    for k in keywords:
        parts.append(f'ti:"{k}"')
        parts.append(f'abs:"{k}"')
    return " OR ".join(parts)


def clean(text):
    """arXiv text is full of line breaks and double spaces. Squash them."""
    return " ".join(text.split())


def fetch_arxiv(keywords, max_results=50):
    """Return a list of paper dicts, newest first."""
    params = {
        "search_query": build_query(keywords),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)

    # Download the results. timeout stops it from hanging forever if arXiv is slow.
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # crash loudly on errors like 500 instead of silently continuing

    # arXiv answers in Atom (an XML feed format). feedparser turns it into Python objects.
    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        papers.append({
            "title": clean(entry.title),
            "authors": [a.name for a in entry.get("authors", [])],
            "abstract": clean(entry.summary),
            "url": entry.link,
            "date": entry.published[:10],  # "2026-11-06T17:59:01Z" -> "2026-11-06"
            "source": "arXiv",
        })
    return papers


if __name__ == "__main__":
    # This block only runs when you run this file directly, not when radar.py imports it.
    from config import KEYWORDS

    papers = fetch_arxiv(KEYWORDS, max_results=20)
    print(f"Got {len(papers)} papers from arXiv\n")
    for i, p in enumerate(papers, 1):
        print(f"{i:2}. [{p['date']}] {p['title']}")
        print(f"    {p['url']}")

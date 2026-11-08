"""Fetch recent bioRxiv preprints that match our keywords and categories.

Run this file on its own to test it:  python biorxiv_source.py
"""
import datetime as dt

import requests

BIORXIV_API = "https://api.biorxiv.org/details/biorxiv"


def matches(item, keywords_lower, categories):
    """True if the paper is in one of our categories AND mentions a keyword."""
    if item.get("category", "").strip().lower() not in categories:
        return False
    text = (item.get("title", "") + " " + item.get("abstract", "")).lower()
    return any(k in text for k in keywords_lower)


def fetch_biorxiv(keywords, categories, days_back=2):
    """Return a list of paper dicts from the last `days_back` days."""
    end = dt.date.today()
    start = end - dt.timedelta(days=days_back)
    keywords_lower = [k.lower() for k in keywords]

    papers = []
    seen_dois = set()  # the same paper can show up twice if it was revised (v1, v2)
    cursor = 0         # bioRxiv returns 100 papers per page; cursor says where to start

    for _ in range(50):  # safety limit: never loop more than 50 pages
        url = f"{BIORXIV_API}/{start}/{end}/{cursor}"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        batch = data.get("collection", [])
        if not batch:
            break

        for item in batch:
            doi = item.get("doi")
            if doi in seen_dois or not matches(item, keywords_lower, categories):
                continue
            seen_dois.add(doi)
            papers.append({
                "title": item.get("title", "").strip(),
                "authors": [a.strip() for a in item.get("authors", "").split(";") if a.strip()],
                "abstract": item.get("abstract", "").strip(),
                "url": f"https://www.biorxiv.org/content/{doi}",
                "date": item.get("date", ""),
                "source": "bioRxiv",
            })

        cursor += len(batch)
        total = int(data.get("messages", [{}])[0].get("total", 0))
        if cursor >= total:
            break

    return papers


if __name__ == "__main__":
    from config import KEYWORDS, BIORXIV_CATEGORIES, DAYS_BACK

    papers = fetch_biorxiv(KEYWORDS, BIORXIV_CATEGORIES, DAYS_BACK)
    print(f"Got {len(papers)} matching papers from bioRxiv\n")
    for i, p in enumerate(papers, 1):
        print(f"{i:2}. [{p['date']}] {p['title']}")
        print(f"    {p['url']}")

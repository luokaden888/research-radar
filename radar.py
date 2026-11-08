"""The main program: pull from every source and show one combined list.

Run:  python radar.py
"""
from arxiv_source import fetch_arxiv
from biorxiv_source import fetch_biorxiv
from config import BIORXIV_CATEGORIES, DAYS_BACK, KEYWORDS, MAX_ARXIV


def collect_papers():
    """Pull from every source and return one list, newest first.

    Split out from main() so other files (like summarize.py) can reuse it.
    """
    papers = []

    # Each source is wrapped in try/except so one broken source
    # doesn't kill the whole run. Real pipelines are built this way.
    try:
        arxiv = fetch_arxiv(KEYWORDS, MAX_ARXIV)
        print(f"arXiv:   {len(arxiv)} papers")
        papers += arxiv
    except Exception as e:
        print(f"arXiv failed: {e}")

    try:
        biorxiv = fetch_biorxiv(KEYWORDS, BIORXIV_CATEGORIES, DAYS_BACK)
        print(f"bioRxiv: {len(biorxiv)} papers")
        papers += biorxiv
    except Exception as e:
        print(f"bioRxiv failed: {e}")

    # Newest first. Dates are "YYYY-MM-DD" strings, which sort correctly as text.
    papers.sort(key=lambda p: p["date"], reverse=True)
    return papers


def main():
    papers = collect_papers()
    print(f"\nTotal: {len(papers)} papers\n")
    for i, p in enumerate(papers, 1):
        print(f"{i:2}. [{p['source']:7}] [{p['date']}] {p['title']}")


if __name__ == "__main__":
    main()

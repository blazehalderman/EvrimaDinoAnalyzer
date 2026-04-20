# etl/extract/scrape_quick_guide.py
# Source 2 extractor — The Isle Evrima Quick Guide (web scrape)
# Method: requests + BeautifulSoup
# Output: data/web_scrape_quick_guide/

import requests
from bs4 import BeautifulSoup
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "web_scrape_quick_guide")


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a page and return a BeautifulSoup parse tree."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_dino_stats(soup: BeautifulSoup) -> list[dict]:
    """Parse dinosaur stat entries from the Quick Guide page structure.

    Returns a list of dicts with fields to be determined once the target
    page structure is confirmed during Phase 1 ETL work.
    """
    raise NotImplementedError("Phase 1 — implement after confirming page structure")


def run():
    """Entry point for Phase 1 ETL: scrape the Quick Guide and write raw output."""
    raise NotImplementedError("Phase 1")


if __name__ == "__main__":
    run()

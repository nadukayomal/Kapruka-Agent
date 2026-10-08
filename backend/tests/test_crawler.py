"""
Crawler tests (Phase 2).

Placeholder until the Playwright scraper is implemented.
"""

from __future__ import annotations

import pytest

from src.crawler.scraper import KaprukaScraper


@pytest.mark.skip(reason="Phase 2 — Playwright crawler not implemented yet")
def test_scraper_returns_products() -> None:
    """
    Scraper should return at least one normalized product.

    Returns:
        None
    """
    products = KaprukaScraper().scrape()
    assert products

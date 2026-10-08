"""
Headless product scraper for kapruka.com.

This module will extract product name, price, description, availability,
category, and URL. Implementation starts in Phase 2.
"""

from __future__ import annotations

from typing import Any


class KaprukaScraper:
    """
    Orchestrates a Playwright session against the Kapruka catalog.
    """

    def scrape(self) -> list[dict[str, Any]]:
        """
        Crawl the live catalog.

        Returns:
            list[dict]: Normalized product records.

        Raises:
            NotImplementedError: Until Phase 2 is implemented.
        """
        raise NotImplementedError("KaprukaScraper.scrape is implemented in Phase 2.")

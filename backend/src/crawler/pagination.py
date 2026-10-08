"""
Pagination and infinite-scroll helpers for the Kapruka crawler.

This module will walk category pages and collect next-page URLs. Implemented
in Phase 2.
"""

from __future__ import annotations


class PaginationWalker:
    """
    Discovers subsequent listing pages from a category URL.
    """

    def next_pages(self, start_url: str) -> list[str]:
        """
        Return listing URLs to visit after ``start_url``.

        Args:
            start_url: First category or search URL.

        Returns:
            list[str]: Additional page URLs.

        Raises:
            NotImplementedError: Until Phase 2 is implemented.
        """
        raise NotImplementedError("PaginationWalker.next_pages is implemented in Phase 2.")

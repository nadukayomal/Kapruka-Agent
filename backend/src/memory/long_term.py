"""
Long-term catalog memory backed by Qdrant (RAG).

Indexes ``data/catalog.json`` and retrieves relevant gifts. Implemented in
Phase 3.
"""

from __future__ import annotations

from typing import Any


class LongTermMemory:
    """
    Vector search over the Kapruka product catalog.
    """

    def search(self, query: str, *, limit: int = 8) -> list[dict[str, Any]]:
        """
        Retrieve catalog items similar to ``query``.

        Args:
            query: Natural-language gift request.
            limit: Maximum number of hits.

        Returns:
            list[dict]: Product payloads with scores.

        Raises:
            NotImplementedError: Until Phase 3 is implemented.
        """
        raise NotImplementedError("LongTermMemory.search is implemented in Phase 3.")

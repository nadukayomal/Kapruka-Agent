"""
Catalog specialist: RAG search over Kapruka products.

Implemented in Phase 4.
"""

from __future__ import annotations

from typing import Any


class CatalogSpecialist:
    """
    Finds gift candidates that match the request and remembered preferences.
    """

    def recommend(self, query: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Return ranked catalog items.

        Args:
            query: User gift request.
            profile: Recipient semantic memory.

        Returns:
            list[dict]: Candidate products.

        Raises:
            NotImplementedError: Until Phase 4 is implemented.
        """
        raise NotImplementedError("CatalogSpecialist.recommend is implemented in Phase 4.")

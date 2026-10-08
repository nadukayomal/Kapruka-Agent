"""
Drafts an initial gift recommendation reply.

Implemented in Phase 5.
"""

from __future__ import annotations

from typing import Any


class Drafter:
    """
    Produces the first-pass assistant response.
    """

    def draft(self, context: dict[str, Any]) -> str:
        """
        Write a draft recommendation.

        Args:
            context: Router output, catalog hits, profile, and user message.

        Returns:
            str: Draft reply.

        Raises:
            NotImplementedError: Until Phase 5 is implemented.
        """
        raise NotImplementedError("Drafter.draft is implemented in Phase 5.")

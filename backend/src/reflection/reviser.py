"""
Revises an unsafe or misaligned draft into a safe recommendation.

Implemented in Phase 5. If no safe option exists, the reviser must refuse
rather than recommend an allergen-containing product.
"""

from __future__ import annotations

from typing import Any


class Reviser:
    """
    Applies critic feedback to produce the final user-facing reply.
    """

    def revise(self, draft: str, critique: dict[str, Any]) -> str:
        """
        Produce a corrected reply.

        Args:
            draft: Original draft text.
            critique: Critic verdict.

        Returns:
            str: Final reply.

        Raises:
            NotImplementedError: Until Phase 5 is implemented.
        """
        raise NotImplementedError("Reviser.revise is implemented in Phase 5.")

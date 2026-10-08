"""
Critiques a draft against allergies, preferences, and delivery constraints.

Implemented in Phase 5.
"""

from __future__ import annotations

from typing import Any


class Critic:
    """
    Scores a draft for safety and preference alignment.
    """

    def critique(self, draft: str, profile: dict[str, Any]) -> dict[str, Any]:
        """
        Review ``draft`` for policy violations.

        Args:
            draft: First-pass assistant text.
            profile: Recipient semantic memory (allergies, likes, district).

        Returns:
            dict: Verdict with issues list and ``safe`` flag.

        Raises:
            NotImplementedError: Until Phase 5 is implemented.
        """
        raise NotImplementedError("Critic.critique is implemented in Phase 5.")

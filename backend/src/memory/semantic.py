"""
Semantic memory: durable recipient profiles (allergies, preferences).

Profiles are JSON documents under ``data/recipient_profiles/``. Implemented
in Phase 3.
"""

from __future__ import annotations

from typing import Any


class SemanticMemory:
    """
    Load and update recipient preference profiles.
    """

    def get_profile(self, recipient_id: str) -> dict[str, Any]:
        """
        Load a recipient profile by identifier.

        Args:
            recipient_id: Stable id such as ``mother_kandy``.

        Returns:
            dict: Profile document.

        Raises:
            NotImplementedError: Until Phase 3 is implemented.
        """
        raise NotImplementedError("SemanticMemory.get_profile is implemented in Phase 3.")

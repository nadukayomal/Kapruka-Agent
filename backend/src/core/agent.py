"""
Main orchestration loop for the Kapruka Gift Concierge.

This module will wire router → specialists → reflection (Draft → Critique →
Revise) using plain Python. No multi-agent framework is used. Implemented in
Phase 6.
"""

from __future__ import annotations

from typing import Any, Iterator


class KaprukaGiftAgent:
    """
    Session-scoped gift concierge that streams thinking and memory events.
    """

    def run(self, message: str, *, session_id: str, recipient_id: str) -> dict[str, Any]:
        """
        Handle one user turn and return the final reply plus traces.

        Args:
            message: User text.
            session_id: Short-term memory key.
            recipient_id: Semantic profile key.

        Returns:
            dict: ``reply``, ``thinking`` steps, and ``memory_recall``.

        Raises:
            NotImplementedError: Until Phase 6 is implemented.
        """
        raise NotImplementedError("KaprukaGiftAgent.run is implemented in Phase 6.")

    def stream(self, message: str, *, session_id: str, recipient_id: str) -> Iterator[dict[str, Any]]:
        """
        Yield thinking / memory / token events for the frontend panels.

        Args:
            message: User text.
            session_id: Short-term memory key.
            recipient_id: Semantic profile key.

        Yields:
            dict: Event payloads.

        Raises:
            NotImplementedError: Until Phase 6 is implemented.
        """
        raise NotImplementedError("KaprukaGiftAgent.stream is implemented in Phase 6.")
        yield from ()  # pragma: no cover — keeps the method typed as a generator

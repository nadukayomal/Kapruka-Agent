"""
Intent router for user messages.

Classifies requests (catalog search, delivery check, preference update, chit-chat)
and dispatches to a specialist. Implemented in Phase 4.
"""

from __future__ import annotations


class IntentRouter:
    """
    Maps a user utterance to a specialist name.
    """

    def route(self, message: str) -> str:
        """
        Classify ``message``.

        Args:
            message: Latest user text.

        Returns:
            str: Specialist key such as ``catalog`` or ``logistics``.

        Raises:
            NotImplementedError: Until Phase 4 is implemented.
        """
        raise NotImplementedError("IntentRouter.route is implemented in Phase 4.")

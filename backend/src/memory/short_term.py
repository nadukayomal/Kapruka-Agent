"""
Short-term (session) memory buffer.

Stores the current conversation turns for the orchestrator. Implemented in
Phase 3.
"""

from __future__ import annotations

from typing import Any


class ShortTermMemory:
    """
    In-process rolling buffer of chat messages for one session.
    """

    def append(self, role: str, content: str) -> None:
        """
        Append a message to the session buffer.

        Args:
            role: ``user``, ``assistant``, or ``system``.
            content: Message text.

        Returns:
            None

        Raises:
            NotImplementedError: Until Phase 3 is implemented.
        """
        raise NotImplementedError("ShortTermMemory.append is implemented in Phase 3.")

    def messages(self) -> list[dict[str, Any]]:
        """
        Return buffered messages in chronological order.

        Returns:
            list[dict]: Chat messages.

        Raises:
            NotImplementedError: Until Phase 3 is implemented.
        """
        raise NotImplementedError("ShortTermMemory.messages is implemented in Phase 3.")

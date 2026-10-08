"""
Memory tests (Phase 3).

Placeholder until short-term, Qdrant, and semantic memory are implemented.
"""

from __future__ import annotations

import pytest

from src.memory.short_term import ShortTermMemory


@pytest.mark.skip(reason="Phase 3 — cognitive memory not implemented yet")
def test_short_term_appends_messages() -> None:
    """
    Session buffer should retain user and assistant turns.

    Returns:
        None
    """
    memory = ShortTermMemory()
    memory.append("user", "Gift for Amma in Kandy, nut-free")
    assert memory.messages()

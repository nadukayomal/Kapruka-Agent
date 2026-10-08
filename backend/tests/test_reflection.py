"""
Reflection-loop tests (Phase 5).

Placeholder until Draft → Critique → Revise is implemented. Nut-free
blocking is a required invariant of that phase.
"""

from __future__ import annotations

import pytest

from src.reflection.critic import Critic


@pytest.mark.skip(reason="Phase 5 — reflection loop not implemented yet")
def test_critic_blocks_nut_products_for_allergy() -> None:
    """
    A draft that recommends cashews must be marked unsafe for nut-free profiles.

    Returns:
        None
    """
    verdict = Critic().critique(
        "I recommend the cashew hamper.",
        {"allergies": ["nuts"], "nut_free": True},
    )
    assert verdict["safe"] is False

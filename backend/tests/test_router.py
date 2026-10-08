"""
Intent router tests (Phase 4).

Placeholder until the specialist router is implemented.
"""

from __future__ import annotations

import pytest

from src.agents.router import IntentRouter


@pytest.mark.skip(reason="Phase 4 — intent router not implemented yet")
def test_router_classifies_catalog_intent() -> None:
    """
    Gift-shopping messages should route to the catalog specialist.

    Returns:
        None
    """
    intent = IntentRouter().route("Find a birthday cake for my mother")
    assert intent == "catalog"

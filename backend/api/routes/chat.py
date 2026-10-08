"""
Chat HTTP routes for the Next.js concierge UI.

Implemented in Phase 7. The router exists now so ``main.py`` can try to
include it without failing the health server.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/status")
def chat_status() -> dict[str, str]:
    """
    Report that the chat specialist pipeline is not wired yet.

    Returns:
        dict: Phase marker.
    """
    return {"status": "not_implemented", "phase": "7"}

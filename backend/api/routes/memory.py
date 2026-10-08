"""
Memory HTTP routes (profiles and session recall) for the frontend panel.

Implemented in Phase 7.
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/memory", tags=["memory"])


@router.get("/status")
def memory_status() -> dict[str, str]:
    """
    Report that memory APIs are not wired yet.

    Returns:
        dict: Phase marker.
    """
    return {"status": "not_implemented", "phase": "7"}

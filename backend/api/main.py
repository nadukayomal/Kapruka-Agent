"""
FastAPI entrypoint for the Kapruka Gift Agent.

Wires CORS, health checks, and routers. Full chat/memory routes land in
Phase 7; Phase 1 exposes a health endpoint so the process can be started.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `uvicorn backend.api.main:app` from the repo root.
_BACKEND = Path(__file__).resolve().parents[1]
_SRC = _BACKEND / "src"
for extra in (str(_BACKEND), str(_SRC)):
    if extra not in sys.path:
        sys.path.insert(0, extra)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utils.config import get_settings
from src.utils.logger import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)
settings = get_settings()

app = FastAPI(
    title="Kapruka Gift Agent",
    version="0.1.0",
    description="Gift concierge API for Kapruka.com (Sri Lanka).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """
    Liveness probe used by scripts and local development.

    Returns:
        dict: Status and environment name.
    """
    return {"status": "ok", "env": settings.app_env}


def _include_routers() -> None:
    """
    Register chat and memory routers when they are implemented (Phase 7).

    Returns:
        None
    """
    try:
        from api.routes.chat import router as chat_router
        from api.routes.memory import router as memory_router

        app.include_router(chat_router)
        app.include_router(memory_router)
    except Exception as exc:
        logger.warning("routers_not_ready", error=str(exc))


_include_routers()

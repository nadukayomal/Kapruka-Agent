"""
Start the FastAPI backend for local development.

Usage (from repository root, with venv activated)::

    python scripts/run_backend.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SRC = BACKEND / "src"
for extra in (str(ROOT), str(BACKEND), str(SRC)):
    if extra not in sys.path:
        sys.path.insert(0, extra)


def main() -> None:
    """
    Boot uvicorn using settings from `.env`.

    Returns:
        None
    """
    import uvicorn

    from src.utils.config import get_settings
    from src.utils.logger import configure_logging, get_logger

    configure_logging()
    settings = get_settings()
    log = get_logger(__name__)
    log.info(
        "backend.starting",
        host=settings.backend_host,
        port=settings.backend_port,
        env=settings.app_env,
    )
    uvicorn.run(
        "api.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.app_env == "development",
        app_dir=str(BACKEND),
    )


if __name__ == "__main__":
    main()

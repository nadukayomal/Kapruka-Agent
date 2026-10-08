"""
Pytest fixtures shared across backend tests.

Ensures ``backend`` and ``backend/src`` are on ``sys.path`` even if pytest
is invoked without pytest.ini.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_BACKEND = Path(__file__).resolve().parents[1]
_SRC = _BACKEND / "src"
for extra in (str(_BACKEND), str(_SRC)):
    if extra not in sys.path:
        sys.path.insert(0, extra)


@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Repository root (directory that contains ``.env.example``).

    Returns:
        Path: Project root.
    """
    from src.utils.config import find_project_root

    return find_project_root()

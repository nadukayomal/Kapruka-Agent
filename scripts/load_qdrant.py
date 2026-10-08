"""
Index ``data/catalog.json`` into Qdrant.

Implemented in Phase 3.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))


def main() -> int:
    """
    Upsert catalog embeddings into the configured Qdrant collection.

    Returns:
        int: Process exit code.
    """
    from src.utils.logger import configure_logging, get_logger

    configure_logging()
    log = get_logger(__name__)
    log.warning("qdrant_load.not_implemented", phase=3)
    print("Phase 3 is not implemented yet. Confirm Phase 1, then complete the crawler.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

"""
CLI entry for the Kapruka catalog crawler.

Implemented in Phase 2. Running it now exits with a clear message.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))


def main() -> int:
    """
    Invoke the scraper and write ``data/catalog.json``.

    Returns:
        int: Process exit code.
    """
    from src.utils.logger import configure_logging, get_logger

    configure_logging()
    log = get_logger(__name__)
    log.warning("crawler.not_implemented", phase=2)
    print("Phase 2 is not implemented yet. Confirm Phase 1 before starting the crawler.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

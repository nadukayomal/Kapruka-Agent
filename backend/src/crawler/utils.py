"""
Crawler-specific parsing helpers (price cleanup, availability flags).

Implemented in Phase 2. Shared text helpers live in ``src.utils.helpers``.
"""

from __future__ import annotations


def parse_price_lkr(raw: str) -> float | None:
    """
    Parse a Sri Lankan Rupee price string into a float.

    Args:
        raw: Display price such as ``Rs. 4,500.00``.

    Returns:
        float | None: Numeric amount, or None if unparsable.

    Raises:
        NotImplementedError: Until Phase 2 is implemented.
    """
    raise NotImplementedError("parse_price_lkr is implemented in Phase 2.")

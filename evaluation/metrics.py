"""
Evaluation metrics for crawl quality, preference alignment, and latency.

Implemented in Phase 9. This module defines the public metric functions so
notebooks and CI can import a stable API.
"""

from __future__ import annotations

from typing import Any, Iterable


def crawl_success_rate(*, attempted: int, succeeded: int) -> float:
    """
    Fraction of listing/product fetches that produced a valid record.

    Args:
        attempted: Total fetch attempts.
        succeeded: Attempts that parsed into a catalog item.

    Returns:
        float: Ratio in [0, 1].

    Raises:
        ValueError: If ``attempted`` is negative or ``succeeded`` exceeds it.
    """
    if attempted < 0 or succeeded < 0 or succeeded > attempted:
        raise ValueError("Invalid crawl counters")
    if attempted == 0:
        return 0.0
    return succeeded / attempted


def preference_alignment_rate(results: Iterable[dict[str, Any]]) -> float:
    """
    Fraction of scenarios whose recommendations respected allergies.

    Args:
        results: Per-scenario dicts with a boolean ``aligned`` field.

    Returns:
        float: Ratio in [0, 1].
    """
    rows = list(results)
    if not rows:
        return 0.0
    hits = sum(1 for row in rows if row.get("aligned"))
    return hits / len(rows)


def summarize_latency_ms(samples_ms: list[float]) -> dict[str, float]:
    """
    Compute simple latency stats for agent turns.

    Args:
        samples_ms: End-to-end durations in milliseconds.

    Returns:
        dict: count, mean, p50, p95 (p95 equals max when n < 20).
    """
    if not samples_ms:
        return {"count": 0.0, "mean": 0.0, "p50": 0.0, "p95": 0.0}
    ordered = sorted(samples_ms)
    n = len(ordered)
    p50 = ordered[n // 2]
    p95_index = min(n - 1, max(0, int(n * 0.95) - 1))
    return {
        "count": float(n),
        "mean": sum(ordered) / n,
        "p50": float(p50),
        "p95": float(ordered[p95_index]),
    }

"""
General helper utilities used across crawler, memory, and the agent loop.

This file provides JSON persistence, text normalization, retry with backoff,
and Sri Lankan district name matching so later specialists share one
implementation instead of copying ad hoc helpers.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any, Callable, TypeVar
from urllib.parse import urljoin, urlparse

from src.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")
SequenceLike = list[str] | tuple[str, ...] | set[str]

# Canonical district names used by Kapruka / Sri Lankan delivery.
SRI_LANKA_DISTRICTS: tuple[str, ...] = (
    "Ampara",
    "Anuradhapura",
    "Badulla",
    "Batticaloa",
    "Colombo",
    "Galle",
    "Gampaha",
    "Hambantota",
    "Jaffna",
    "Kalutara",
    "Kandy",
    "Kegalle",
    "Kilinochchi",
    "Kurunegala",
    "Mannar",
    "Matale",
    "Matara",
    "Monaragala",
    "Mullaitivu",
    "Nuwara Eliya",
    "Polonnaruwa",
    "Puttalam",
    "Ratnapura",
    "Trincomalee",
    "Vavuniya",
)


class JsonStore:
    """
    Load and save UTF-8 JSON files with directories created on write.
    """

    @staticmethod
    def load(path: Path, default: Any | None = None) -> Any:
        """
        Read JSON from disk.

        Args:
            path: File path.
            default: Value to return if the file does not exist.

        Returns:
            Any: Parsed JSON document.

        Raises:
            FileNotFoundError: If the file is missing and no default is given.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        if not path.is_file():
            if default is not None:
                return default
            raise FileNotFoundError(f"JSON file not found: {path}")
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @staticmethod
    def save(path: Path, payload: Any, *, indent: int = 2) -> None:
        """
        Write JSON to disk, creating parent directories as needed.

        Args:
            path: Destination file path.
            payload: JSON-serializable object.
            indent: Pretty-print indent.

        Returns:
            None
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=indent)
            handle.write("\n")
        logger.debug("json.saved", path=str(path))


class TextNormalizer:
    """
    String helpers for slugs, whitespace, and allergy keyword matching.
    """

    _slug_pattern = re.compile(r"[^a-z0-9]+")
    _ws_pattern = re.compile(r"\s+")

    @classmethod
    def slugify(cls, value: str) -> str:
        """
        Convert a string to a lowercase hyphenated slug.

        Args:
            value: Raw label (product name, district, etc.).

        Returns:
            str: Slug, or ``item`` if nothing remains after cleaning.
        """
        lowered = value.strip().lower()
        slug = cls._slug_pattern.sub("-", lowered).strip("-")
        return slug or "item"

    @classmethod
    def collapse_whitespace(cls, value: str) -> str:
        """
        Collapse internal whitespace and trim ends.

        Args:
            value: Raw text, possibly with newlines from HTML.

        Returns:
            str: Single-line cleaned text.
        """
        return cls._ws_pattern.sub(" ", value).strip()

    @classmethod
    def contains_any(cls, haystack: str, needles: SequenceLike) -> bool:
        """
        Return True if any needle appears in ``haystack`` (case-insensitive).

        Args:
            haystack: Text to search (for example a product description).
            needles: Allergy or preference keywords.

        Returns:
            bool: True when at least one needle is present.
        """
        blob = haystack.lower()
        return any(needle.lower() in blob for needle in needles if needle)


class RetryPolicy:
    """
    Simple exponential backoff for network calls (crawler, Qdrant, OpenAI).
    """

    def __init__(
        self,
        *,
        attempts: int = 3,
        base_delay_seconds: float = 0.5,
        retry_on: tuple[type[BaseException], ...] = (Exception,),
    ) -> None:
        """
        Configure retry behaviour.

        Args:
            attempts: Total tries including the first.
            base_delay_seconds: Delay after the first failure; doubles each time.
            retry_on: Exception types that trigger a retry.
        """
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self.attempts = attempts
        self.base_delay_seconds = base_delay_seconds
        self.retry_on = retry_on

    def run(self, fn: Callable[[], T], *, operation: str = "call") -> T:
        """
        Execute ``fn`` until it succeeds or attempts are exhausted.

        Args:
            fn: Zero-argument callable.
            operation: Label used in logs.

        Returns:
            T: Return value of ``fn``.

        Raises:
            BaseException: The last exception if all attempts fail.
        """
        last_error: BaseException | None = None
        for attempt in range(1, self.attempts + 1):
            try:
                return fn()
            except self.retry_on as exc:
                last_error = exc
                if attempt == self.attempts:
                    break
                delay = self.base_delay_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "retry.backoff",
                    operation=operation,
                    attempt=attempt,
                    delay_seconds=delay,
                    error=str(exc),
                )
                time.sleep(delay)
        assert last_error is not None
        raise last_error


class UrlHelper:
    """
    URL joining and host checks for the Kapruka crawler.
    """

    @staticmethod
    def join(base: str, href: str) -> str:
        """
        Resolve a possibly relative href against a base URL.

        Args:
            base: Absolute page or site URL.
            href: Absolute or relative link.

        Returns:
            str: Absolute URL.
        """
        return urljoin(base, href)

    @staticmethod
    def is_http_url(value: str) -> bool:
        """
        Return True if ``value`` looks like an http(s) URL.

        Args:
            value: Candidate string.

        Returns:
            bool: True for http/https URLs.
        """
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


class DistrictMatcher:
    """
    Normalize free-text locations to Sri Lankan district names.
    """

    def __init__(self, districts: tuple[str, ...] = SRI_LANKA_DISTRICTS) -> None:
        """
        Args:
            districts: Canonical district list.
        """
        self._by_lower = {name.lower(): name for name in districts}

    def match(self, text: str) -> str | None:
        """
        Find a district mentioned in ``text``.

        Args:
            text: User message or address fragment (for example ``Kandy``).

        Returns:
            str | None: Canonical district name, or None if unmatched.
        """
        lowered = text.lower()
        for key, canonical in self._by_lower.items():
            if key in lowered:
                return canonical
        return None

    def is_known(self, district: str) -> bool:
        """
        Check whether ``district`` is a known Sri Lankan district.

        Args:
            district: Candidate name.

        Returns:
            bool: True if the name is in the canonical list.
        """
        return district.strip().lower() in self._by_lower

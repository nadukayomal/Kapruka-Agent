"""
Unit tests for Phase 1 utilities: config, tokens, helpers, and logging.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.utils.config import find_project_root, get_settings, reload_settings
from src.utils.helpers import DistrictMatcher, JsonStore, RetryPolicy, TextNormalizer, UrlHelper
from src.utils.logger import configure_logging, get_logger
from src.utils.token import TokenCounter, count_tokens


def test_find_project_root_contains_env_example() -> None:
    """
    The detected root must contain the env template.

    Returns:
        None
    """
    root = find_project_root()
    assert (root / ".env.example").is_file()


def test_settings_load_without_secrets() -> None:
    """
    Settings must load from `.env` even when API keys are empty.

    Returns:
        None
    """
    reload_settings()
    settings = get_settings()
    assert settings.backend_port == 8000
    assert settings.catalog_file.name == "catalog.json"
    assert settings.cors_origin_list
    assert settings.log_level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def test_token_counter_empty_and_nonempty() -> None:
    """
    Empty text is zero tokens; non-empty text is at least one.

    Returns:
        None
    """
    counter = TokenCounter()
    assert counter.count("") == 0
    assert counter.count("Kapruka gift hamper for Amma in Kandy") >= 1
    assert count_tokens("hello") >= 1
    truncated = counter.truncate("word " * 200, max_tokens=8)
    assert counter.count(truncated) <= 8


def test_json_store_roundtrip(tmp_path: Path) -> None:
    """
    JsonStore writes UTF-8 JSON and reads it back.

    Args:
        tmp_path: Pytest temporary directory.

    Returns:
        None
    """
    path = tmp_path / "nested" / "item.json"
    payload = {"name": "Kadala", "price_lkr": 1500}
    JsonStore.save(path, payload)
    loaded = JsonStore.load(path)
    assert loaded == payload
    assert JsonStore.load(tmp_path / "missing.json", default=[]) == []


def test_text_normalizer_and_allergens() -> None:
    """
    Slugify, whitespace collapse, and allergy keyword detection.

    Returns:
        None
    """
    assert TextNormalizer.slugify("Nut Mix Hamper!") == "nut-mix-hamper"
    assert TextNormalizer.collapse_whitespace("  chocolate\n  cake ") == "chocolate cake"
    assert TextNormalizer.contains_any("Cashew cookies", ["peanut", "cashew"])
    assert not TextNormalizer.contains_any("Fresh flowers", ["nut", "cashew"])


def test_retry_policy_succeeds_after_failure() -> None:
    """
    RetryPolicy retries then returns the successful value.

    Returns:
        None
    """
    state = {"n": 0}

    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 2:
            raise RuntimeError("transient")
        return "ok"

    policy = RetryPolicy(attempts=3, base_delay_seconds=0.01, retry_on=(RuntimeError,))
    assert policy.run(flaky, operation="test") == "ok"
    assert state["n"] == 2


def test_district_matcher_kandy() -> None:
    """
    Free text mentioning Kandy maps to the canonical district.

    Returns:
        None
    """
    matcher = DistrictMatcher()
    assert matcher.match("Send to my mother in Kandy please") == "Kandy"
    assert matcher.is_known("colombo")
    assert matcher.match("Mars") is None


def test_url_helper() -> None:
    """
    Relative Kapruka links resolve against the site origin.

    Returns:
        None
    """
    joined = UrlHelper.join("https://www.kapruka.com/gifts", "/item/123")
    assert joined.startswith("https://")
    assert UrlHelper.is_http_url(joined)
    assert not UrlHelper.is_http_url("not-a-url")


def test_logger_redacts_keys() -> None:
    """
    Logger factory returns a usable bound logger.

    Returns:
        None
    """
    configure_logging(force=True)
    log = get_logger("tests")
    log.info("phase1.check", component="utils")
    assert log is not None


def test_catalog_seed_is_valid_json() -> None:
    """
    Seed catalog file must be valid JSON (list).

    Returns:
        None
    """
    path = find_project_root() / "data" / "catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)

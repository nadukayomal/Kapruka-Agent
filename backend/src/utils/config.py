"""
Application configuration for the Kapruka Gift Agent.

This file loads `.env` from the project root, validates every setting with
Pydantic, and exposes a single cached ``Settings`` instance. Call
``get_settings()`` from other modules; do not read ``os.environ`` ad hoc.

Secrets (API keys) are required to come from the environment. Empty strings
are allowed in local development so Phase 1 tests can run without credentials.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_project_root(start: Path | None = None) -> Path:
    """
    Walk upward from ``start`` until a directory that contains ``.env.example``.

    Args:
        start: Directory to begin the search. Defaults to this file's folder.

    Returns:
        Path: Absolute path of the repository root.

    Raises:
        FileNotFoundError: If no ancestor contains ``.env.example``.
    """
    current = (start or Path(__file__).resolve()).parent
    for candidate in (current, *current.parents):
        if (candidate / ".env.example").is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate project root (missing .env.example). "
        "Run the application from the Kapruka Gift Agent repository."
    )


class Settings(BaseSettings):
    """
    Typed runtime configuration.

    Values are read from environment variables and an optional ``.env`` file
    at the project root. Field names map to uppercase env vars by default.
    """

    model_config = SettingsConfigDict(
        env_file=str(find_project_root() / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="development", description="Runtime environment name.")
    log_level: str = Field(default="INFO", description="Python / structlog log level.")
    log_json: bool = Field(default=True, description="Emit JSON logs when true.")
    backend_host: str = Field(default="127.0.0.1")
    backend_port: int = Field(default=8000, ge=1, le=65535)
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed browser origins.",
    )

    openai_api_key: str = Field(default="", description="OpenAI or compatible API key.")
    openai_base_url: str = Field(default="https://api.openai.com/v1")
    openai_model: str = Field(default="gpt-4o-mini")
    openai_embedding_model: str = Field(default="text-embedding-3-small")

    max_context_tokens: int = Field(default=8000, ge=256)
    max_completion_tokens: int = Field(default=1024, ge=16)

    qdrant_url: str = Field(default="http://127.0.0.1:6333")
    qdrant_api_key: str = Field(default="")
    qdrant_collection: str = Field(default="kapruka_catalog")
    qdrant_memory_collection: str = Field(default="kapruka_memory")

    catalog_path: str = Field(default="data/catalog.json")
    recipient_profiles_dir: str = Field(default="data/recipient_profiles")
    sample_conversations_dir: str = Field(default="data/sample_conversations")

    kapruka_base_url: str = Field(default="https://www.kapruka.com")
    crawler_headless: bool = Field(default=True)
    crawler_max_pages: int = Field(default=50, ge=1)
    crawler_request_timeout_ms: int = Field(default=30_000, ge=1000)

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        """
        Normalize log level to an uppercase logging name.

        Args:
            value: Raw log level from the environment.

        Returns:
            str: One of DEBUG, INFO, WARNING, ERROR, CRITICAL.

        Raises:
            ValueError: If the value is not a known level.
        """
        level = value.strip().upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {sorted(allowed)}")
        return level

    @property
    def project_root(self) -> Path:
        """
        Return the repository root path.

        Returns:
            Path: Absolute project root.
        """
        return find_project_root()

    @property
    def cors_origin_list(self) -> List[str]:
        """
        Split ``CORS_ORIGINS`` into a list of origin URLs.

        Returns:
            list[str]: Trimmed origin strings, empty entries dropped.
        """
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

    def resolve_path(self, relative_or_absolute: str) -> Path:
        """
        Resolve a configured path against the project root when it is relative.

        Args:
            relative_or_absolute: Path from settings or a caller.

        Returns:
            Path: Absolute filesystem path.
        """
        path = Path(relative_or_absolute)
        if path.is_absolute():
            return path
        return (self.project_root / path).resolve()

    @property
    def catalog_file(self) -> Path:
        """
        Absolute path to the product catalog JSON file.

        Returns:
            Path: Catalog file location.
        """
        return self.resolve_path(self.catalog_path)

    @property
    def profiles_dir(self) -> Path:
        """
        Absolute path to the recipient profile directory.

        Returns:
            Path: Profiles directory.
        """
        return self.resolve_path(self.recipient_profiles_dir)

    def require_openai_key(self) -> str:
        """
        Return the OpenAI key or fail fast when a later phase needs an LLM.

        Returns:
            str: Non-empty API key.

        Raises:
            RuntimeError: If ``OPENAI_API_KEY`` is missing.
        """
        if not self.openai_api_key.strip():
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to `.env` before calling the LLM."
            )
        return self.openai_api_key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Load and cache application settings.

    Returns:
        Settings: Process-wide configuration object.
    """
    return Settings()


def reload_settings() -> Settings:
    """
    Drop the settings cache and reload from the environment.

    Useful in tests after mutating env vars.

    Returns:
        Settings: Freshly loaded configuration.
    """
    get_settings.cache_clear()
    return get_settings()

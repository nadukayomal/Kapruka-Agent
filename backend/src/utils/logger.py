"""
Structured logging for the Kapruka Gift Agent.

This file configures structlog once per process and returns bound loggers
with a consistent JSON (or console) format. Use ``get_logger(__name__)`` at
module import time. Extra fields (session_id, recipient_id) can be bound
per request in the FastAPI layer later.
"""

from __future__ import annotations

import logging
import sys
from typing import Any, MutableMapping, Optional

import structlog

from src.utils.config import get_settings

_CONFIGURED = False


def configure_logging(force: bool = False) -> None:
    """
    Initialize stdlib logging and structlog processors.

    Safe to call multiple times; subsequent calls are no-ops unless
    ``force=True``.

    Args:
        force: Reconfigure even if logging was already set up.

    Returns:
        None
    """
    global _CONFIGURED
    if _CONFIGURED and not force:
        return

    settings = get_settings()
    level = getattr(logging, settings.log_level, logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
        force=True,
    )

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_json:
        renderer: Any = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )
    root = logging.getLogger()
    if root.handlers:
        root.handlers[0].setFormatter(formatter)

    _CONFIGURED = True


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Return a named structured logger.

    Args:
        name: Logger name, typically ``__name__``.

    Returns:
        BoundLogger: Structlog logger bound to the given name.
    """
    configure_logging()
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """
    Bind request-scoped fields to all subsequent log events in this context.

    Args:
        **kwargs: Key/value pairs such as ``session_id`` or ``recipient_id``.

    Returns:
        None
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """
    Clear request-scoped logging context.

    Returns:
        None
    """
    structlog.contextvars.clear_contextvars()


def log_event(
    logger: structlog.stdlib.BoundLogger,
    event: str,
    *,
    level: str = "info",
    **fields: Any,
) -> None:
    """
    Emit a single named event with structured fields.

    Args:
        logger: Logger instance from ``get_logger``.
        event: Short event name (for example ``catalog.search``).
        level: Log level name (debug, info, warning, error).
        **fields: Additional structured payload.

    Returns:
        None
    """
    method = getattr(logger, level.lower(), logger.info)
    method(event, **_sanitize(fields))


def _sanitize(fields: MutableMapping[str, Any] | dict[str, Any]) -> dict[str, Any]:
    """
    Drop obviously sensitive keys from a log payload.

    Args:
        fields: Arbitrary structured fields.

    Returns:
        dict: Copy of fields with secret-like keys redacted.
    """
    blocked = {"api_key", "openai_api_key", "qdrant_api_key", "authorization", "password"}
    cleaned: dict[str, Any] = {}
    for key, value in fields.items():
        if key.lower() in blocked:
            cleaned[key] = "***"
        else:
            cleaned[key] = value
    return cleaned


class LoggerMixin:
    """
    Mixin that gives a class a lazy ``self.logger`` bound to the class module.
    """

    _logger: Optional[structlog.stdlib.BoundLogger] = None

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """
        Return a logger named after the concrete class module.

        Returns:
            BoundLogger: Cached structured logger.
        """
        if self._logger is None:
            self._logger = get_logger(self.__class__.__module__)
        return self._logger

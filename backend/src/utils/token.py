"""
Token counting and truncation utilities.

This file wraps tiktoken so the agent can budget prompt size before calling
an LLM. If tiktoken cannot load an encoding for a model, a conservative
character-based estimate is used so the rest of the stack still works.
"""

from __future__ import annotations

from typing import Iterable, Sequence

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Conservative fallback: ~4 characters per token for English/Sinhala mix.
_CHARS_PER_TOKEN = 4


class TokenCounter:
    """
    Count and truncate text using a model-specific tokenizer when available.
    """

    def __init__(self, model: str | None = None) -> None:
        """
        Create a counter for a given chat or embedding model.

        Args:
            model: OpenAI-compatible model name. Defaults to settings.openai_model.
        """
        from src.utils.config import get_settings

        self.model = model or get_settings().openai_model
        self._encoding = self._load_encoding(self.model)

    @staticmethod
    def _load_encoding(model: str) -> object | None:
        """
        Load a tiktoken encoding for ``model``.

        Args:
            model: Model identifier.

        Returns:
            Encoding | None: tiktoken encoding, or None if unavailable.
        """
        try:
            import tiktoken
        except ImportError:
            logger.warning("tiktoken_missing", model=model)
            return None

        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            try:
                return tiktoken.get_encoding("cl100k_base")
            except Exception as exc:  # pragma: no cover - encoder package broken
                logger.warning("tiktoken_encoding_failed", error=str(exc), model=model)
                return None

    def count(self, text: str) -> int:
        """
        Count tokens in a string.

        Args:
            text: Input text.

        Returns:
            int: Token count (estimated if no encoder is available).
        """
        if not text:
            return 0
        if self._encoding is None:
            return max(1, (len(text) + _CHARS_PER_TOKEN - 1) // _CHARS_PER_TOKEN)
        return len(self._encoding.encode(text))  # type: ignore[union-attr]

    def count_messages(self, messages: Sequence[dict[str, str]]) -> int:
        """
        Approximate tokens for a chat-completions message list.

        Uses a small per-message overhead consistent with OpenAI chat formats.

        Args:
            messages: List of ``{"role": ..., "content": ...}`` dicts.

        Returns:
            int: Estimated total tokens.
        """
        total = 0
        for message in messages:
            total += 4  # role/name/separator overhead
            total += self.count(str(message.get("content", "")))
            total += self.count(str(message.get("role", "")))
        return total + 2  # reply priming

    def truncate(self, text: str, max_tokens: int) -> str:
        """
        Truncate ``text`` so it fits within ``max_tokens``.

        Args:
            text: Source text.
            max_tokens: Inclusive token budget.

        Returns:
            str: Original or truncated text.
        """
        if max_tokens <= 0 or not text:
            return ""
        if self.count(text) <= max_tokens:
            return text

        if self._encoding is not None:
            tokens = self._encoding.encode(text)  # type: ignore[union-attr]
            return self._encoding.decode(tokens[:max_tokens])  # type: ignore[union-attr]

        char_budget = max_tokens * _CHARS_PER_TOKEN
        return text[:char_budget]

    def truncate_to_budget(
        self,
        chunks: Iterable[str],
        max_tokens: int,
        *,
        separator: str = "\n",
    ) -> str:
        """
        Concatenate chunks until the token budget is exhausted.

        Args:
            chunks: Ordered text fragments (for example catalog hits).
            max_tokens: Inclusive token budget for the joined result.
            separator: String inserted between chunks.

        Returns:
            str: Joined text that fits the budget.
        """
        kept: list[str] = []
        used = 0
        sep_cost = self.count(separator)
        for chunk in chunks:
            cost = self.count(chunk)
            extra = sep_cost if kept else 0
            if used + extra + cost > max_tokens:
                remaining = max_tokens - used - extra
                if remaining > 0:
                    kept.append(self.truncate(chunk, remaining))
                break
            kept.append(chunk)
            used += extra + cost
        return separator.join(kept)


def count_tokens(text: str, model: str | None = None) -> int:
    """
    Convenience function to count tokens without managing a ``TokenCounter``.

    Args:
        text: Input text.
        model: Optional model name.

    Returns:
        int: Token count.
    """
    return TokenCounter(model).count(text)

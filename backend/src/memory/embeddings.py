"""
Embedding client for catalog and memory vectors.

Wraps the OpenAI-compatible embeddings API. Implemented in Phase 3.
"""

from __future__ import annotations


class EmbeddingClient:
    """
    Produce dense vectors for RAG indexing and query.
    """

    def embed(self, texts: list[str]) -> list[list[float]]:
        """
        Embed one or more texts.

        Args:
            texts: Strings to embed.

        Returns:
            list[list[float]]: Embedding vectors aligned with ``texts``.

        Raises:
            NotImplementedError: Until Phase 3 is implemented.
        """
        raise NotImplementedError("EmbeddingClient.embed is implemented in Phase 3.")

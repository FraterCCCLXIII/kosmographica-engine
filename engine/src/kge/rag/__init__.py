"""Retrieval seam for grounded authoring (Wave 2).

``Retriever`` is the swappable interface the LLM author grounds against. Wave 2
ships :class:`KeywordRetriever` (Postgres FTS + 1-hop graph expansion). A
``VectorRetriever`` over ``entities.embedding`` is a Wave 3 drop-in that
implements the same protocol — no author/verifier changes required.
"""

from .retriever import KeywordRetriever, Retriever

__all__ = ["Retriever", "KeywordRetriever"]

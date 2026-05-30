"""Tiny lexical-similarity helpers shared by the verifier and the offline fake LLM.

Deliberately dependency-free and deterministic. The real entailment signal comes
from an ``LLMClient`` in Wave 2; these functions back the lexical baseline (the
gate the LLM must beat) and the offline ``FakeLLMClient``.
"""

from __future__ import annotations

import re

_WORD = re.compile(r"\w+")
_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "to", "is", "are", "was", "were",
    "as", "by", "for", "with", "at", "from", "that", "this", "it", "its", "be", "his",
    "her", "their", "who", "which", "but", "not", "also", "such", "than", "into",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def content_tokens(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if w not in _STOPWORDS and len(w) > 1}


def lexical_overlap(assertion: str, evidence: str | list[str]) -> float:
    """Fraction of the assertion's content tokens present in the evidence."""
    a = content_tokens(assertion)
    if not a:
        return 0.0
    if isinstance(evidence, str):
        evidence = [evidence]
    e: set[str] = set()
    for chunk in evidence:
        e |= content_tokens(chunk)
    return len(a & e) / len(a)

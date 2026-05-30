"""Deterministic, offline LLM client for tests, CI, and local development.

* ``entail`` returns the lexical overlap between hypothesis and premise — the same
  signal as the lexical baseline, so the loop behaves predictably without a model.
* ``generate`` replays scripted responses when provided (handy for asserting on a
  specific author output); otherwise it falls back to a deterministic heuristic
  that extracts grounded claims as JSON, so the LLM author is exercisable offline.

No network, no secrets, no randomness.
"""

from __future__ import annotations

import json
import re
from collections import deque

from ..textsim import lexical_overlap

_SENTENCE = re.compile(r"(?<=[.!?])\s+")
# The author prompt embeds the source text between these sentinels (see authoring.py).
_SOURCE_BLOCK = re.compile(r"<source>(.*?)</source>", re.DOTALL)


class FakeLLMClient:
    name = "fake-llm"

    def __init__(self, responses: list[str] | None = None, *, max_claims: int = 5, min_len: int = 20):
        self._scripted: deque[str] = deque(responses or [])
        self.max_claims = max_claims
        self.min_len = min_len

    def entail(self, premise: str, hypothesis: str) -> float:
        return round(lexical_overlap(hypothesis, premise), 4)

    def generate(self, prompt: str, *, system: str | None = None, max_tokens: int = 512) -> str:
        if self._scripted:
            return self._scripted.popleft()
        return self._heuristic_author(prompt)

    def _heuristic_author(self, prompt: str) -> str:
        """Mimic an extraction author: emit JSON claims grounded in the source block."""
        match = _SOURCE_BLOCK.search(prompt)
        text = match.group(1).strip() if match else prompt
        sentences = [s.strip() for s in _SENTENCE.split(text) if len(s.strip()) >= self.min_len]
        claims = [{"assertion": s, "quotes": [s]} for s in sentences[: self.max_claims]]
        return json.dumps(claims)

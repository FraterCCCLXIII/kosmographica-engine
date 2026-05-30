"""Shared prompt + parser for asking a generative model for an entailment score.

Hosted/instruction-tuned models don't expose an NLI head, so we ask for a single
number and parse it defensively. A dedicated NLI model can replace this by
implementing ``LLMClient.entail`` directly.
"""

from __future__ import annotations

import re

ENTAIL_SYSTEM = (
    "You are a strict fact-checker. Given SOURCE text and a CLAIM, decide how fully the "
    "SOURCE supports the CLAIM. Reply with ONLY a number from 0.0 (not supported / "
    "contradicted) to 1.0 (fully and explicitly supported). No words."
)


def entail_prompt(premise: str, hypothesis: str) -> str:
    return f"SOURCE:\n{premise}\n\nCLAIM:\n{hypothesis}\n\nScore (0.0-1.0):"


_NUM = re.compile(r"[01](?:\.\d+)?|0?\.\d+")


def parse_score(text: str) -> float:
    match = _NUM.search(text)
    if not match:
        return 0.0
    try:
        return max(0.0, min(1.0, float(match.group(0))))
    except ValueError:  # pragma: no cover - defensive
        return 0.0

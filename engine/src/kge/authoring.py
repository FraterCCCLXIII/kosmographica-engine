"""AI authoring — produce *grounded* contribution envelopes (ADR-013, step 1).

An author may not assert what it did not retrieve: every proposed claim carries the exact
source span(s) it is grounded in. This module defines the author contract and a
deterministic, offline stand-in (``SentenceAuthor``) so the whole publish-then-verify loop
is testable without a live LLM. A real LLM-backed author implements the same `Author`
protocol — emit assertions plus the verbatim source spans that support them.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from .envelope import ClaimIn, Envelope, SourceIn, SupportSpan
from .textsim import normalize


@dataclass
class SourceDoc:
    """A retrieved source the author grounds against (and the verifier re-reads)."""

    ref: str
    citation: str
    text: str
    uri: str | None = None


@dataclass
class ProposedClaim:
    assertion: str
    quotes: list[str] = field(default_factory=list)  # verbatim spans from the source


@runtime_checkable
class Author(Protocol):
    name: str

    def propose(self, source: SourceDoc, about: str) -> list[ProposedClaim]: ...


_SENTENCE = re.compile(r"(?<=[.!?])\s+")


class SentenceAuthor:
    """Offline stand-in for an LLM author: each source sentence becomes a grounded claim
    whose support span is that exact sentence."""

    name = "sentence-author"

    def __init__(self, max_claims: int = 5, min_len: int = 20) -> None:
        self.max_claims = max_claims
        self.min_len = min_len

    def propose(self, source: SourceDoc, about: str) -> list[ProposedClaim]:
        sentences = [s.strip() for s in _SENTENCE.split(source.text) if len(s.strip()) >= self.min_len]
        return [ProposedClaim(assertion=s, quotes=[s]) for s in sentences[: self.max_claims]]


_AUTHOR_SYSTEM = (
    "You are a careful encyclopedia author. Extract only claims that are explicitly "
    "stated in the SOURCE. For each claim, return the exact verbatim quote(s) from the "
    "SOURCE that support it. Never invent facts. Respond with ONLY a JSON array of "
    'objects: [{"assertion": "...", "quotes": ["..."]}].'
)


def _author_prompt(source: SourceDoc, about: str) -> str:
    return (
        f"Subject: {about}\n"
        f"Citation: {source.citation}\n\n"
        f"<source>{source.text}</source>\n\n"
        "Return the grounded claims as a JSON array."
    )


class LLMAuthor:
    """LLM-backed author: prompt a model to extract claims grounded in the source.

    Claims whose quotes are not present verbatim in the source are dropped here
    (the independent verifier enforces the same rule again downstream).
    """

    def __init__(self, client, *, max_claims: int = 8) -> None:
        self._client = client
        self.max_claims = max_claims
        self.name = f"llm-author:{getattr(client, 'name', 'unknown')}"

    def propose(self, source: SourceDoc, about: str) -> list[ProposedClaim]:
        raw = self._client.generate(_author_prompt(source, about), system=_AUTHOR_SYSTEM)
        proposals = self._parse(raw)
        haystack = normalize(source.text)
        grounded: list[ProposedClaim] = []
        for proposal in proposals:
            quotes = [q for q in proposal.quotes if q.strip() and normalize(q) in haystack]
            if proposal.assertion.strip() and quotes:
                grounded.append(ProposedClaim(assertion=proposal.assertion.strip(), quotes=quotes))
            if len(grounded) >= self.max_claims:
                break
        return grounded

    @staticmethod
    def _parse(raw: str) -> list[ProposedClaim]:
        text = raw.strip()
        if text.startswith("```"):  # tolerate fenced code blocks
            text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
        try:
            items = json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return []
        if not isinstance(items, list):
            return []
        out: list[ProposedClaim] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            assertion = str(item.get("assertion", "")).strip()
            quotes_raw = item.get("quotes") or item.get("quote") or []
            if isinstance(quotes_raw, str):
                quotes_raw = [quotes_raw]
            quotes = [str(q) for q in quotes_raw if str(q).strip()]
            if assertion:
                out.append(ProposedClaim(assertion=assertion, quotes=quotes))
        return out


def build_grounded_envelope(
    source: SourceDoc,
    about: str,
    proposals: list[ProposedClaim],
    *,
    generator: str,
    source_system: str = "ai",
    batch_id: str | None = None,
    about_kind: str = "entity",
) -> Envelope:
    """Assemble a grounded (``requires_grounding=True``) envelope from proposed claims.

    ``about`` is an existing canonical KID (e.g. ``kg:entity/...``). The full source text
    is stored on the source so the *independent* verifier can re-read it.
    """
    src = SourceIn(ref=source.ref, citation=source.citation, uri=source.uri, data={"text": source.text})
    claims = [
        ClaimIn(
            about=about,
            about_kind=about_kind,
            assertion=p.assertion,
            source_refs=[source.ref],
            support_spans=[SupportSpan(source_ref=source.ref, quote=q) for q in p.quotes],
        )
        for p in proposals
    ]
    return Envelope(
        source_system=source_system,
        generator=generator,
        batch_id=batch_id,
        requires_grounding=True,
        sources=[src],
        claims=claims,
    )


def author_envelope(
    author: Author,
    source: SourceDoc,
    about: str,
    *,
    source_system: str = "ai",
    batch_id: str | None = None,
    about_kind: str = "entity",
) -> Envelope:
    """Run an author over a source and package the result as a grounded envelope."""
    proposals = author.propose(source, about)
    return build_grounded_envelope(
        source,
        about,
        proposals,
        generator=author.name,
        source_system=source_system,
        batch_id=batch_id,
        about_kind=about_kind,
    )

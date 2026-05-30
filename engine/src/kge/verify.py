"""Publish-then-verify (ADR-013, steps 2-6).

The verifier is *independent* of the author: it re-reads the cited source text and runs
deterministic checks plus an entailment score. The support score becomes the claim's
confidence and routes visibility:

  * fabricated span (not in source) -> reject (stays machine_unverified / hidden)
  * entailment >= threshold        -> accept (promoted to machine_validated / public-badged)
  * otherwise                      -> reject

Every run is recorded in `verifications` so auditing is a query. The entailment scorer
here is a deterministic lexical-overlap stand-in; swap in an NLI model behind
`Verifier(entailment=...)` without changing the loop.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from .envelope import Envelope
from .models import Claim, TrustTier, Verification
from .pipeline import IngestResult, ingest

_WORD = re.compile(r"\w+")
_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "to", "is", "are", "was", "were",
    "as", "by", "for", "with", "at", "from", "that", "this", "it", "its", "be", "his",
    "her", "their", "who", "which", "but", "not", "also", "such", "than", "into",
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _content_tokens(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if w not in _STOPWORDS and len(w) > 1}


def spans_present(quotes: list[str], source_text: str) -> bool:
    """Anti-fabrication: every support span must appear verbatim in the source."""
    haystack = _normalize(source_text)
    return all(_normalize(q) in haystack for q in quotes if q.strip())


def lexical_entailment(assertion: str, quotes: list[str]) -> float:
    """Fraction of the assertion's content tokens supported by the span tokens."""
    assertion_tokens = _content_tokens(assertion)
    if not assertion_tokens:
        return 0.0
    span_tokens: set[str] = set()
    for q in quotes:
        span_tokens |= _content_tokens(q)
    return len(assertion_tokens & span_tokens) / len(assertion_tokens)


@dataclass
class VerificationResult:
    support_label: str  # entailed | not_entailed | fabricated
    support_score: float
    outcome: str  # accept | reject | dispute
    reason: str


class Verifier:
    def __init__(
        self,
        name: str = "lexical-verifier-v0",
        accept_threshold: float = 0.6,
        entailment: Callable[[str, list[str]], float] = lexical_entailment,
    ) -> None:
        self.name = name
        self.accept_threshold = accept_threshold
        self._entailment = entailment

    def verify(self, *, assertion: str, quotes: list[str], source_text: str) -> VerificationResult:
        if not quotes or not spans_present(quotes, source_text):
            return VerificationResult(
                "fabricated", 0.0, "reject", "support span not found verbatim in source"
            )
        score = round(self._entailment(assertion, quotes), 4)
        if score >= self.accept_threshold:
            return VerificationResult("entailed", score, "accept", "entailed by cited source")
        return VerificationResult(
            "not_entailed", score, "reject", f"entailment {score} below {self.accept_threshold}"
        )


@dataclass
class WriteLoopResult:
    batch_id: str
    quarantined: bool = False
    accepted: int = 0
    rejected: int = 0
    ingest: IngestResult | None = None


def _quotes(claim: Claim) -> list[str]:
    return [s.get("quote", "") for s in (claim.support_spans or [])]


def _source_text(claim: Claim) -> str:
    for src in claim.sources:
        text = (src.data or {}).get("text")
        if text:
            return text
    return ""


def _verify_and_route(session: Session, claim: Claim, verifier: Verifier) -> str:
    result = verifier.verify(
        assertion=claim.assertion, quotes=_quotes(claim), source_text=_source_text(claim)
    )
    session.add(
        Verification(
            claim_id=claim.id,
            verifier=verifier.name,
            support_label=result.support_label,
            support_score=result.support_score,
            outcome=result.outcome,
            reason=result.reason,
        )
    )
    claim.confidence = result.support_score
    if result.outcome == "accept":
        claim.tier = TrustTier.MACHINE_VALIDATED  # public, badged
    elif result.outcome == "dispute":
        claim.disputed = True
    else:  # reject -> stays machine_unverified (hidden)
        claim.tier = TrustTier.MACHINE_UNVERIFIED
    return result.outcome


def publish_then_verify(
    session: Session, env: Envelope, verifier: Verifier | None = None
) -> WriteLoopResult:
    """Ingest a grounded envelope, then verify+route each loaded claim (ADR-013)."""
    verifier = verifier or Verifier()
    ingest_result = ingest(session, env)
    if ingest_result.quarantined:
        return WriteLoopResult(batch_id=ingest_result.batch_id, quarantined=True, ingest=ingest_result)

    session.flush()
    claims = session.scalars(
        select(Claim).where(
            Claim.batch_id == ingest_result.batch_id, Claim.generator == env.generator
        )
    ).all()
    accepted = rejected = 0
    for claim in claims:
        outcome = _verify_and_route(session, claim, verifier)
        if outcome == "accept":
            accepted += 1
        elif outcome == "reject":
            rejected += 1
    session.flush()
    return WriteLoopResult(
        batch_id=ingest_result.batch_id, accepted=accepted, rejected=rejected, ingest=ingest_result
    )


def reverify(
    session: Session,
    verifier: Verifier | None = None,
    *,
    batch_id: str | None = None,
    generator: str | None = None,
    tier: str | None = None,
) -> dict[str, int]:
    """Re-check existing claims (by batch/generator/tier), recompute confidence, re-route,
    and record a fresh verification. Supports continuous re-verification / spot audits."""
    verifier = verifier or Verifier()
    where = []
    if batch_id:
        where.append(Claim.batch_id == batch_id)
    if generator:
        where.append(Claim.generator == generator)
    if tier:
        where.append(Claim.tier == tier)
    claims = session.scalars(select(Claim).where(*where)).all()

    summary = {"checked": 0, "accept": 0, "reject": 0, "dispute": 0}
    for claim in claims:
        if not claim.support_spans:
            continue  # only AI-grounded claims are re-verifiable here
        outcome = _verify_and_route(session, claim, verifier)
        summary["checked"] += 1
        summary[outcome] += 1
    session.flush()
    return summary


def mark_disputed(session: Session, claim_id: str, reason: str, verifier: str = "manual") -> None:
    """Open a dispute on a claim — both sides of a contradiction coexist (no AI edit wars)."""
    claim = session.get(Claim, claim_id)
    if claim is None:
        return
    claim.disputed = True
    session.add(
        Verification(
            claim_id=claim_id,
            verifier=verifier,
            support_label="not_entailed",
            support_score=claim.confidence,
            outcome="dispute",
            reason=reason,
        )
    )
    session.flush()

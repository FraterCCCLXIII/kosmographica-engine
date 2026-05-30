"""Continuous re-verification job (W2.3).

Re-checks AI-grounded claims with the configured verifier so confidence and tier
reflect the *current* model (e.g. after a provider/threshold change), decaying or
promoting claims and recording a fresh ``verifications`` row each time. Emits an
**audit delta** — the before/after tier histogram plus outcome counts — so a run is
observable from the audit surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Claim
from ..verify import Verifier, make_llm_verifier, reverify


@dataclass
class ReverifyDelta:
    checked: int = 0
    accept: int = 0
    reject: int = 0
    dispute: int = 0
    tiers_before: dict[str, int] = field(default_factory=dict)
    tiers_after: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict:
        moved = {
            tier: self.tiers_after.get(tier, 0) - self.tiers_before.get(tier, 0)
            for tier in set(self.tiers_before) | set(self.tiers_after)
        }
        return {
            "checked": self.checked,
            "outcomes": {"accept": self.accept, "reject": self.reject, "dispute": self.dispute},
            "tiers_before": self.tiers_before,
            "tiers_after": self.tiers_after,
            "tier_delta": {k: v for k, v in moved.items() if v},
        }


def _grounded_tier_histogram(
    session: Session, *, batch_id: str | None, generator: str | None, tier: str | None
) -> dict[str, int]:
    # Only AI-grounded claims (those carrying support spans) are re-verifiable.
    where = [func.jsonb_array_length(Claim.support_spans) > 0]
    if batch_id:
        where.append(Claim.batch_id == batch_id)
    if generator:
        where.append(Claim.generator == generator)
    if tier:
        where.append(Claim.tier == tier)
    rows = session.execute(
        select(Claim.tier, func.count()).where(*where).group_by(Claim.tier)
    ).all()
    return {t: c for t, c in rows}


def run_reverify(
    session: Session,
    *,
    verifier: Verifier | None = None,
    batch_id: str | None = None,
    generator: str | None = None,
    tier: str | None = None,
) -> ReverifyDelta:
    """Run one re-verification pass and return the audit delta."""
    verifier = verifier or make_llm_verifier()
    before = _grounded_tier_histogram(session, batch_id=batch_id, generator=generator, tier=tier)
    summary = reverify(session, verifier, batch_id=batch_id, generator=generator, tier=tier)
    after = _grounded_tier_histogram(session, batch_id=batch_id, generator=generator, tier=None)
    return ReverifyDelta(
        checked=summary["checked"],
        accept=summary["accept"],
        reject=summary["reject"],
        dispute=summary["dispute"],
        tiers_before=before,
        tiers_after=after,
    )

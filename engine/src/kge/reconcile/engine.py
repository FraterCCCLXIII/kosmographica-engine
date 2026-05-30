"""Reconciliation matcher + ``sameAs`` lifecycle.

Cheapest signal first (entity-resolution.md):

1. **Deterministic** — entities sharing an external authority ID across sources are
   the same; auto-accepted.
2. **Blocking** — group remaining entities by ``(module, type, normalized-label)``.
3. **Scoring** — cross-source pairs in a block are scored by name overlap and land in
   the **review queue** (``proposed``). Name similarity alone never auto-links
   (no cross-tradition auto-merge); a human accepts/rejects.

Accepting a proposal writes a non-destructive ``sameAs`` relationship; rejecting it is
remembered so the pair is not re-proposed.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Entity, ExternalId, Reconciliation, Relationship
from ..textsim import content_tokens

SAMEAS_PREDICATE = "sameAs"
SAMEAS_SOURCE = "reconciliation"


def _norm_label(label: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", label.lower())).strip()


def _name_score(a: str, b: str) -> float:
    ta, tb = content_tokens(a), content_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)  # Jaccard


def _ordered(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


@dataclass
class ProposeSummary:
    deterministic: int = 0
    proposed: int = 0
    skipped_existing: int = 0
    blocks_scanned: int = 0

    def as_dict(self) -> dict:
        return {
            "deterministic": self.deterministic,
            "proposed": self.proposed,
            "skipped_existing": self.skipped_existing,
            "blocks_scanned": self.blocks_scanned,
        }


def _existing_pairs(session: Session) -> set[tuple[str, str]]:
    rows = session.execute(select(Reconciliation.left_kid, Reconciliation.right_kid)).all()
    return {(left, right) for left, right in rows}


def _upsert(
    session: Session,
    seen: set[tuple[str, str]],
    left: Entity,
    right: Entity,
    *,
    method: str,
    score: float,
    status: str,
    reason: str,
) -> bool:
    lk, rk = _ordered(left.id, right.id)
    if (lk, rk) in seen:
        return False
    seen.add((lk, rk))
    # Preserve which source each kid came from regardless of ordering.
    left_src = left.source_system if lk == left.id else right.source_system
    right_src = right.source_system if rk == right.id else left.source_system
    row = Reconciliation(
        left_kid=lk,
        right_kid=rk,
        left_source=left_src,
        right_source=right_src,
        match_method=method,
        score=round(score, 4),
        status=status,
        reason=reason,
    )
    session.add(row)
    if status == "accepted":
        _ensure_sameas(session, lk, rk)
    return True


def propose_matches(session: Session, *, name_threshold: float = 0.6) -> ProposeSummary:
    """Scan the corpus and create reconciliation proposals (idempotent re-runs)."""
    summary = ProposeSummary()
    seen = _existing_pairs(session)

    entities = session.execute(
        select(
            Entity.id, Entity.module, Entity.type, Entity.label, Entity.source_system
        )
    ).all()
    by_id = {e.id: e for e in entities}

    # 1. Deterministic: shared (authority, value) across different kids/sources.
    xrows = session.execute(select(ExternalId.kid, ExternalId.authority, ExternalId.value)).all()
    by_authval: dict[tuple[str, str], list[str]] = defaultdict(list)
    for kid, authority, value in xrows:
        by_authval[(authority, value)].append(kid)
    for kids in by_authval.values():
        for i in range(len(kids)):
            for j in range(i + 1, len(kids)):
                a, b = by_id.get(kids[i]), by_id.get(kids[j])
                if not a or not b or a.source_system == b.source_system:
                    continue
                if _upsert(session, seen, a, b, method="deterministic", score=1.0,
                           status="accepted", reason="shared external authority id"):
                    summary.deterministic += 1

    # 2/3. Blocking by (module, type, normalized label) + cross-source scoring.
    blocks: dict[tuple[str, str, str], list] = defaultdict(list)
    for e in entities:
        blocks[(e.module, e.type, _norm_label(e.label))].append(e)

    for members in blocks.values():
        sources = {m.source_system for m in members}
        if len(members) < 2 or len(sources) < 2:
            continue
        summary.blocks_scanned += 1
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                a, b = members[i], members[j]
                if a.source_system == b.source_system:
                    continue
                score = _name_score(a.label, b.label)
                if score < name_threshold:
                    continue
                lk, rk = _ordered(a.id, b.id)
                if (lk, rk) in seen:
                    summary.skipped_existing += 1
                    continue
                if _upsert(session, seen, a, b, method="scored", score=score, status="proposed",
                           reason=f"name match {a.label!r}~{b.label!r} (review; no auto-merge on name)"):
                    summary.proposed += 1

    session.flush()
    return summary


def _ensure_sameas(session: Session, left_kid: str, right_kid: str) -> None:
    ext = f"sameas:{left_kid}:{right_kid}"
    exists = session.scalar(
        select(Relationship.id).where(
            Relationship.source_system == SAMEAS_SOURCE, Relationship.external_id == ext
        )
    )
    if exists:
        return
    session.add(
        Relationship(
            subject_id=left_kid,
            predicate=SAMEAS_PREDICATE,
            object_id=right_kid,
            data={"reconciled": True},
            source_system=SAMEAS_SOURCE,
            external_id=ext,
            generator="reconciler",
        )
    )


def accept(session: Session, recon_id: int) -> bool:
    row = session.get(Reconciliation, recon_id)
    if row is None or row.status == "accepted":
        return False
    row.status = "accepted"
    row.decided_at = dt.datetime.now(dt.timezone.utc)
    _ensure_sameas(session, row.left_kid, row.right_kid)
    session.flush()
    return True


def reject(session: Session, recon_id: int, reason: str | None = None) -> bool:
    row = session.get(Reconciliation, recon_id)
    if row is None or row.status == "rejected":
        return False
    row.status = "rejected"
    if reason:
        row.reason = reason
    row.decided_at = dt.datetime.now(dt.timezone.utc)
    session.flush()
    return True


def reconciliation_stats(session: Session) -> dict:
    by_status = dict(
        session.execute(
            select(Reconciliation.status, func.count()).group_by(Reconciliation.status)
        ).all()
    )
    by_method = dict(
        session.execute(
            select(Reconciliation.match_method, func.count()).group_by(Reconciliation.match_method)
        ).all()
    )
    return {
        "by_status": by_status,
        "by_method": by_method,
        "total": sum(by_status.values()),
    }

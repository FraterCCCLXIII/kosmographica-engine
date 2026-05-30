"""Audit endpoints — the read surface for the (read-only) Audit Console and for
post-hoc auditing of AI writes (ADR-013).

Unlike the public endpoints these are *not* clamped to the public tier: auditing the AI
means seeing ``machine_unverified`` and ``machine_validated`` records. Filter explicitly
by tier / generator / batch_id so "all machine_validated claims by model X in batch Y" is
a single query.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...models import Claim, Entity, Relationship
from ..deps import get_session
from ..schemas import AuditStats, ClaimAuditOut, Page

router = APIRouter(prefix="/v1/audit", tags=["audit"])


@router.get("/stats", response_model=AuditStats)
def stats(session: Session = Depends(get_session)):
    claims_by_tier = dict(
        session.execute(select(Claim.tier, func.count()).group_by(Claim.tier)).all()
    )
    entities_by_tier = dict(
        session.execute(select(Entity.tier, func.count()).group_by(Entity.tier)).all()
    )
    by_generator = [
        {"generator": g, "tier": t, "count": c}
        for g, t, c in session.execute(
            select(Claim.generator, Claim.tier, func.count())
            .group_by(Claim.generator, Claim.tier)
            .order_by(func.count().desc())
        ).all()
    ]
    disputes = session.scalar(select(func.count()).select_from(Claim).where(Claim.disputed))
    return AuditStats(
        claims_by_tier=claims_by_tier,
        entities_by_tier=entities_by_tier,
        claims_by_generator=by_generator,
        disputes=disputes or 0,
    )


def _attach_labels(session: Session, claims: list[Claim]) -> list[ClaimAuditOut]:
    entity_ids = [c.about_id for c in claims if c.about_kind == "entity"]
    rel_ids = [c.about_id for c in claims if c.about_kind == "relationship"]
    labels: dict[str, str] = {}
    if entity_ids:
        labels.update(
            dict(
                session.execute(
                    select(Entity.id, Entity.label).where(Entity.id.in_(entity_ids))
                ).all()
            )
        )
    if rel_ids:
        labels.update(
            dict(
                session.execute(
                    select(Relationship.id, Relationship.predicate).where(
                        Relationship.id.in_(rel_ids)
                    )
                ).all()
            )
        )
    out = []
    for c in claims:
        item = ClaimAuditOut.model_validate(c)
        item.about_label = labels.get(c.about_id)
        out.append(item)
    return out


@router.get("/claims", response_model=Page)
def list_claims(
    session: Session = Depends(get_session),
    tier: str | None = Query(None, description="Exact tier, e.g. machine_validated (the queue)"),
    generator: str | None = None,
    batch_id: str | None = None,
    disputed: bool | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    where = []
    if tier:
        where.append(Claim.tier == tier)
    if generator:
        where.append(Claim.generator == generator)
    if batch_id:
        where.append(Claim.batch_id == batch_id)
    if disputed is not None:
        where.append(Claim.disputed.is_(disputed))

    total = session.scalar(select(func.count()).select_from(Claim).where(*where))
    claims = session.scalars(
        select(Claim).where(*where).order_by(Claim.recorded_at.desc()).limit(limit).offset(offset)
    ).all()
    return Page(items=_attach_labels(session, claims), total=total or 0, limit=limit, offset=offset)


@router.get("/disputes", response_model=Page)
def list_disputes(
    session: Session = Depends(get_session),
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    return list_claims(session=session, disputed=True, limit=limit, offset=offset)


@router.get("/claims/{kid:path}", response_model=ClaimAuditOut)
def get_claim(kid: str, session: Session = Depends(get_session)):
    claim = session.get(Claim, kid)
    if claim is None:
        raise HTTPException(status_code=404, detail="claim not found")
    return _attach_labels(session, [claim])[0]

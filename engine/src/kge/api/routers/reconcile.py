"""Reconciliation read endpoints (W2.2) — the review queue + parity for the console.

Read-only, consistent with the Wave 2 stance (AI-only writes, observation-only
console). Accept/reject decisions are operator actions via the ``kge reconcile``
CLI; a human web action layer is deferred to Wave 3.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ...models import Entity, Reconciliation
from ...reconcile import reconciliation_stats, source_parity
from ..deps import get_session
from ..schemas import (
    Page,
    ReconciliationOut,
    ReconciliationStats,
    ReconEntityOut,
    SourceParityOut,
)

router = APIRouter(prefix="/v1/reconcile", tags=["reconcile"])

# Sources whose convergence we report by default.
KNOWN_SOURCES = ["mythographica", "sacred_lineage"]


@router.get("/stats", response_model=ReconciliationStats)
def stats(session: Session = Depends(get_session)):
    return ReconciliationStats(**reconciliation_stats(session))


@router.get("/proposals", response_model=Page)
def list_proposals(
    session: Session = Depends(get_session),
    status: str | None = Query("proposed", description="proposed | accepted | rejected | all"),
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    where = []
    if status and status != "all":
        where.append(Reconciliation.status == status)
    total = session.scalar(
        select(func.count()).select_from(Reconciliation).where(*where)
    )
    rows = session.scalars(
        select(Reconciliation)
        .where(*where)
        .order_by(Reconciliation.score.desc(), Reconciliation.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return Page(items=_hydrate(session, rows), total=total or 0, limit=limit, offset=offset)


@router.get("/parity", response_model=list[SourceParityOut])
def parity(session: Session = Depends(get_session)):
    return [SourceParityOut(**source_parity(session, s)) for s in KNOWN_SOURCES]


def _hydrate(session: Session, rows: list[Reconciliation]) -> list[ReconciliationOut]:
    kids = {r.left_kid for r in rows} | {r.right_kid for r in rows}
    entities = {}
    if kids:
        entities = {
            e.id: e
            for e in session.scalars(select(Entity).where(Entity.id.in_(kids))).all()
        }
    out: list[ReconciliationOut] = []
    for r in rows:
        item = ReconciliationOut.model_validate(r)
        left, right = entities.get(r.left_kid), entities.get(r.right_kid)
        item.left = ReconEntityOut.model_validate(left) if left else None
        item.right = ReconEntityOut.model_validate(right) if right else None
        out.append(item)
    return out

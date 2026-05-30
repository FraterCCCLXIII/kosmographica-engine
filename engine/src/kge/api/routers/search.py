"""Full-text entity search (Postgres FTS, ADR-006)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...models import Entity
from ...search import fts_match, fts_rank
from ..deps import PUBLIC_SENSITIVITIES, get_session, visible_tiers
from ..schemas import EntityOut, SearchHitOut

router = APIRouter(prefix="/v1/search", tags=["search"])


@router.get("", response_model=list[SearchHitOut])
def search(
    q: str = Query(min_length=1),
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
    limit: int = Query(20, le=100),
):
    rank = fts_rank(q)
    rows = session.execute(
        select(Entity, rank.label("rank"))
        .where(
            fts_match(q),
            Entity.tier.in_(tiers),
            Entity.sensitivity.in_(PUBLIC_SENSITIVITIES),
        )
        .order_by(rank.desc())
        .limit(limit)
    ).all()
    return [
        SearchHitOut(entity=EntityOut.model_validate(entity), rank=float(score))
        for entity, score in rows
    ]

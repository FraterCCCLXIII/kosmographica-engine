"""Entity read endpoints: detail, list/filter, and 1-hop graph neighborhood."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ...lineage import (
    LINEAGE_VIEW_TYPES,
    load_lineage_out,
    pick_lineage_chart,
    resolve_lineage_charts,
)
from ...models import Claim, Entity, Relationship
from ..deps import PUBLIC_SENSITIVITIES, get_session, visible_tiers
from ..schemas import (
    ClaimOut,
    EntityDetailOut,
    EntityOut,
    GraphOut,
    LineageOut,
    Page,
    RelationshipOut,
)

router = APIRouter(prefix="/v1/entities", tags=["entities"])


@router.get("", response_model=Page)
def list_entities(
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
    module: str | None = None,
    type: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    where = [Entity.tier.in_(tiers), Entity.sensitivity.in_(PUBLIC_SENSITIVITIES)]
    if module:
        where.append(Entity.module == module)
    if type:
        where.append(Entity.type == type)

    total = session.scalar(select(func.count()).select_from(Entity).where(*where))
    rows = session.scalars(
        select(Entity).where(*where).order_by(Entity.label).limit(limit).offset(offset)
    ).all()
    return Page(
        items=[EntityOut.model_validate(r) for r in rows],
        total=total or 0,
        limit=limit,
        offset=offset,
    )


def _get_visible_entity(session: Session, kid: str, tiers: list[str]) -> Entity:
    entity = session.get(Entity, kid)
    if entity is None or entity.tier not in tiers or entity.sensitivity not in PUBLIC_SENSITIVITIES:
        raise HTTPException(status_code=404, detail="entity not found")
    return entity


@router.get("/by-slug/{module}/{type}/{slug}", response_model=EntityDetailOut)
def get_entity_by_slug(
    module: str,
    type: str,
    slug: str,
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
):
    # The slug ends in the 6-hex KID suffix (schemas.EntityOut.slug); resolve by it.
    suffix = slug.rsplit("-", 1)[-1]
    entity = session.scalar(
        select(Entity).where(
            Entity.module == module,
            Entity.type == type,
            Entity.id.like(f"%{suffix}"),
            Entity.tier.in_(tiers),
            Entity.sensitivity.in_(PUBLIC_SENSITIVITIES),
        )
    )
    if entity is None:
        raise HTTPException(status_code=404, detail="entity not found")
    return _entity_detail(session, entity, tiers)


@router.get("/{kid:path}/lineage", response_model=LineageOut)
def entity_lineage(
    kid: str,
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
):
    entity = _get_visible_entity(session, kid, tiers)
    if entity.type not in LINEAGE_VIEW_TYPES:
        raise HTTPException(status_code=404, detail="entity type has no lineage view")

    charts = resolve_lineage_charts(
        session, entity, tiers=tiers, public_sensitivities=PUBLIC_SENSITIVITIES
    )
    chart = pick_lineage_chart(session, charts, tiers=tiers)
    if chart is None:
        raise HTTPException(status_code=404, detail="no lineage chart for entity")

    return load_lineage_out(
        session, chart, tiers=tiers, public_sensitivities=PUBLIC_SENSITIVITIES
    )


@router.get("/{kid:path}/graph", response_model=GraphOut)
def entity_graph(
    kid: str,
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
):
    _get_visible_entity(session, kid, tiers)  # 404s if the root entity isn't visible
    edges = session.scalars(
        select(Relationship).where(
            or_(Relationship.subject_id == kid, Relationship.object_id == kid),
            Relationship.tier.in_(tiers),
        )
    ).all()
    neighbor_ids = {e.subject_id for e in edges} | {e.object_id for e in edges} | {kid}
    nodes = session.scalars(
        select(Entity).where(
            Entity.id.in_(neighbor_ids),
            Entity.tier.in_(tiers),
            Entity.sensitivity.in_(PUBLIC_SENSITIVITIES),
        )
    ).all()
    visible = {n.id for n in nodes}
    return GraphOut(
        nodes=[EntityOut.model_validate(n) for n in nodes],
        edges=[
            RelationshipOut.model_validate(e)
            for e in edges
            if e.subject_id in visible and e.object_id in visible
        ],
    )


@router.get("/{kid:path}", response_model=EntityDetailOut)
def get_entity(
    kid: str,
    session: Session = Depends(get_session),
    tiers: list[str] = Depends(visible_tiers),
):
    entity = _get_visible_entity(session, kid, tiers)
    return _entity_detail(session, entity, tiers)


def _entity_detail(session: Session, entity: Entity, tiers: list[str]) -> EntityDetailOut:
    claims = session.scalars(
        select(Claim)
        .where(
            Claim.about_id == entity.id,
            Claim.about_kind == "entity",
            Claim.tier.in_(tiers),
            Claim.sensitivity.in_(PUBLIC_SENSITIVITIES),
        )
        .order_by(Claim.confidence.desc())
    ).all()
    detail = EntityDetailOut.model_validate(entity)
    detail.claims = [ClaimOut.model_validate(c) for c in claims]
    return detail

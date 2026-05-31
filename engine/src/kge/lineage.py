"""Build transmission trees for LineageChart entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session

from kge.models import Entity, Relationship

if TYPE_CHECKING:
    from kge.api.schemas import LineageNodeOut, LineageOut

LINEAGE_VIEW_TYPES = frozenset({"LineageChart", "School", "Tradition"})
HAS_LINEAGE_CHART = "has_lineage_chart"


def _chart_ref(entity: Entity) -> str | None:
    return entity.external_id or None


def _scoped_transmissions(
    chart: Entity, relationships: list[Relationship]
) -> list[Relationship]:
    ref = _chart_ref(chart)
    if not ref:
        return []
    return [r for r in relationships if (r.data or {}).get("lineage_chart") == ref]


def _build_subtree(
    node_id: str,
    children_map: dict[str, list[tuple[str, str]]],
    entities_by_id: dict[str, Entity],
    visiting: set[str],
) -> LineageNodeOut | None:
    from kge.api.schemas import EntityOut, LineageNodeOut

    entity = entities_by_id.get(node_id)
    if entity is None:
        return None
    if node_id in visiting:
        return LineageNodeOut(entity=EntityOut.model_validate(entity), children=[])
    visiting.add(node_id)
    children: list[LineageNodeOut] = []
    for child_id, predicate in children_map.get(node_id, []):
        child = _build_subtree(child_id, children_map, entities_by_id, visiting)
        if child is not None:
            child.predicate = predicate
            children.append(child)
    visiting.remove(node_id)
    return LineageNodeOut(entity=EntityOut.model_validate(entity), children=children)


def build_lineage_out(
    chart: Entity,
    relationships: list[Relationship],
    entities: list[Entity],
) -> LineageOut:
    from kge.api.schemas import EntityOut, LineageOut

    transmissions = _scoped_transmissions(chart, relationships)
    entities_by_id = {e.id: e for e in entities}

    children_map: dict[str, list[tuple[str, str]]] = {}
    child_ids: set[str] = set()
    figure_ids: set[str] = set()

    for rel in transmissions:
        if rel.subject_id not in entities_by_id or rel.object_id not in entities_by_id:
            continue
        figure_ids.add(rel.subject_id)
        figure_ids.add(rel.object_id)
        child_ids.add(rel.object_id)
        children_map.setdefault(rel.subject_id, []).append((rel.object_id, rel.predicate))

    root_ids = [fid for fid in figure_ids if fid not in child_ids]
    if not root_ids and figure_ids:
        # Cycle or ambiguous graph — pick a stable root (earliest valid_from, else label).
        root_ids = [
            sorted(
                figure_ids,
                key=lambda fid: (
                    entities_by_id[fid].valid_from is None,
                    entities_by_id[fid].valid_from or 0,
                    entities_by_id[fid].label,
                ),
            )[0]
        ]

    roots: list[LineageNodeOut] = []
    tree_ids: set[str] = set()

    def collect_ids(node: LineageNodeOut) -> None:
        tree_ids.add(node.entity.id)
        for child in node.children:
            collect_ids(child)

    for root_id in sorted(root_ids, key=lambda fid: entities_by_id[fid].label):
        node = _build_subtree(root_id, children_map, entities_by_id, set())
        if node is not None:
            roots.append(node)
            collect_ids(node)

    unlinked = [
        EntityOut.model_validate(entities_by_id[fid])
        for fid in sorted(figure_ids - tree_ids, key=lambda fid: entities_by_id[fid].label)
        if fid in entities_by_id
    ]

    return LineageOut(
        chart=EntityOut.model_validate(chart),
        roots=roots,
        unlinked=unlinked,
        transmission_count=len(transmissions),
    )


def external_numeric_id(external_id: str | None) -> str | None:
    if not external_id or ":" not in external_id:
        return None
    return external_id.rsplit(":", 1)[-1]


def resolve_lineage_charts(
    session: Session,
    entity: Entity,
    *,
    tiers: list[str],
    public_sensitivities: list[str],
) -> list[Entity]:
    if entity.type == "LineageChart":
        return [entity]
    if entity.type not in {"School", "Tradition"}:
        return []

    visible = [
        Entity.tier.in_(tiers),
        Entity.type == "LineageChart",
        Entity.sensitivity.in_(public_sensitivities),
    ]

    rels = session.scalars(
        select(Relationship).where(
            Relationship.subject_id == entity.id,
            Relationship.predicate == HAS_LINEAGE_CHART,
            Relationship.tier.in_(tiers),
        )
    ).all()
    if rels:
        chart_ids = [r.object_id for r in rels]
        charts = session.scalars(select(Entity).where(Entity.id.in_(chart_ids), *visible)).all()
        if charts:
            return list(charts)

    suffix = external_numeric_id(entity.external_id)
    if suffix is None:
        return []
    data_key = "school_id" if entity.type == "School" else "tradition_id"
    charts = session.scalars(
        select(Entity).where(
            *visible,
            Entity.source_system == entity.source_system,
            Entity.data[data_key].astext == suffix,
        )
    ).all()
    return list(charts)


def pick_lineage_chart(
    session: Session,
    charts: list[Entity],
    *,
    tiers: list[str],
) -> Entity | None:
    if not charts:
        return None
    if len(charts) == 1:
        return charts[0]

    best = charts[0]
    best_count = -1
    for chart in charts:
        chart_ref = chart.external_id
        if not chart_ref:
            continue
        transmissions = session.scalars(
            select(Relationship).where(
                Relationship.tier.in_(tiers),
                Relationship.source_system == chart.source_system,
                Relationship.data["lineage_chart"].astext == chart_ref,
            )
        ).all()
        n = len(transmissions)
        if n > best_count:
            best_count = n
            best = chart
    return best


def load_lineage_out(
    session: Session,
    chart: Entity,
    *,
    tiers: list[str],
    public_sensitivities: list[str],
) -> LineageOut:
    chart_ref = chart.external_id
    if not chart_ref:
        return build_lineage_out(chart, [], [])

    transmissions = session.scalars(
        select(Relationship).where(
            Relationship.tier.in_(tiers),
            Relationship.source_system == chart.source_system,
            Relationship.data["lineage_chart"].astext == chart_ref,
        )
    ).all()
    if not transmissions:
        return build_lineage_out(chart, [], [])

    figure_ids = {r.subject_id for r in transmissions} | {r.object_id for r in transmissions}
    entities = session.scalars(
        select(Entity).where(
            Entity.id.in_(figure_ids),
            Entity.tier.in_(tiers),
            Entity.sensitivity.in_(public_sensitivities),
        )
    ).all()
    return build_lineage_out(chart, list(transmissions), list(entities))

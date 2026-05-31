"""Sacred-Lineage source adapter (second federated source, Wave 2 / W2.2).

Sacred-Lineage is a Prisma/SQLite app of spiritual figures, traditions, schools,
texts, concepts, and transmission lineages. This adapter maps its tables into a
contribution envelope. It is a *federated source import* (``requires_grounding=
False``): claims carry citations, not grounded spans.

**Partial-tolerant by design** (the source is known-incomplete): rows missing a
usable name are skipped (and counted), empty tables are fine, and null fields are
simply omitted — a thin source never fails the batch or overrides another source.

Two entry points:
  * :func:`load_sqlite` — read the relevant tables from a Sacred-Lineage SQLite DB
    into a plain dict (stdlib only), so the mapping is testable without the DB.
  * :func:`sacred_lineage_to_envelope` — map that dict into an :class:`Envelope`.

See `../../../docs/architecture/entity-resolution.md` and
`../../../docs/program/migration-and-convergence.md` (row c).
"""

from __future__ import annotations

import sqlite3
from typing import Any

from ..envelope import ClaimIn, EntityIn, Envelope, ExternalIdIn, RelationshipIn, SourceIn

MODULE = "religion-mythology"  # shared namespace so Concepts/Deities reconcile with Mythographica
SOURCE_SYSTEM = "sacred_lineage"
DEFAULT_CITATION = "Sacred-Lineage dataset"

# Tables read by load_sqlite (omitted/empty tables are tolerated).
_TABLES = (
    "traditions",
    "schools",
    "lineage_charts",
    "masters",
    "relationship_types",
    "relationships",
    "entity_links",
    "concepts",
    "texts",
    "practices",
    "institutions",
    "places",
    "historical_periods",
    "events",
)

# Sacred-Lineage entity_link source/target type -> our ref table key.
_LINK_TYPE_TO_TABLE = {
    "concept": "concept",
    "text": "text",
    "figure": "figure",
    "master": "figure",
    "tradition": "tradition",
    "school": "school",
    "practice": "practice",
    "institution": "institution",
    "place": "place",
}


def load_sqlite(path: str) -> dict[str, list[dict[str, Any]]]:
    """Read the relevant Sacred-Lineage tables into ``{table: [rows...]}``."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    tables: dict[str, list[dict[str, Any]]] = {}
    try:
        present = {
            r[0] for r in conn.execute("select name from sqlite_master where type='table'")
        }
        for table in _TABLES:
            if table in present:
                tables[table] = [dict(row) for row in conn.execute(f"select * from {table}")]
            else:
                tables[table] = []
    finally:
        conn.close()
    return tables


def _ref(table: str, row_id: Any) -> str:
    return f"sl:{table}:{row_id}"


def _clean(value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _split_tags(value: Any) -> list[str]:
    if not value or not isinstance(value, str):
        return []
    parts = [p.strip() for p in value.replace(";", ",").split(",")]
    return [p for p in parts if p]


class _SourcePool:
    """Deduplicate citation strings into envelope sources with stable refs."""

    def __init__(self) -> None:
        self._by_citation: dict[str, str] = {}
        self.sources: list[SourceIn] = []
        self.default_ref = self.ref_for(DEFAULT_CITATION)

    def ref_for(self, citation: str, uri: str | None = None) -> str:
        citation = (citation or "").strip() or DEFAULT_CITATION
        if citation in self._by_citation:
            return self._by_citation[citation]
        ref = f"src_{len(self.sources)}"
        self._by_citation[citation] = ref
        self.sources.append(SourceIn(ref=ref, citation=citation, uri=uri, source_system=SOURCE_SYSTEM))
        return ref


def sacred_lineage_to_envelope(
    tables: dict[str, list[dict[str, Any]]],
    *,
    generator: str = "sacred-lineage-adapter",
    batch_id: str | None = None,
) -> Envelope:
    """Map Sacred-Lineage tables into a federated contribution envelope."""
    pool = _SourcePool()
    entities: list[EntityIn] = []
    relationships: list[RelationshipIn] = []
    claims: list[ClaimIn] = []
    skipped = 0

    # Index of refs we actually emitted, so relationships only wire valid endpoints.
    emitted: set[str] = set()

    def add_entity(
        table: str,
        row: dict,
        *,
        etype: str,
        label_key: str,
        desc_key: str | None,
        data: dict | None = None,
        valid_from: int | None = None,
        valid_to: int | None = None,
        external_ids: list[ExternalIdIn] | None = None,
        citation_ref: str | None = None,
    ) -> str | None:
        nonlocal skipped
        label = _clean(row.get(label_key))
        if not label:
            skipped += 1
            return None
        ref = _ref(table, row["id"])
        payload = {k: v for k, v in (data or {}).items() if v not in (None, "", [], {})}
        native = _clean(row.get("name_native")) or _clean(row.get("title_native"))
        if native:
            payload["name_native"] = native
        desc = _clean(row.get(desc_key)) if desc_key else None
        if desc:
            payload["description"] = desc
        entities.append(
            EntityIn(
                ref=ref,
                external_id=ref,
                module=MODULE,
                type=etype,
                label=label,
                data=payload,
                valid_from=valid_from,
                valid_to=valid_to,
                external_ids=external_ids or [],
            )
        )
        emitted.add(ref)
        if desc:
            claims.append(
                ClaimIn(
                    about=ref,
                    about_kind="entity",
                    assertion=desc,
                    source_refs=[citation_ref or pool.default_ref],
                )
            )
        return ref

    for row in tables.get("traditions", []):
        add_entity(
            "tradition", row, etype="Tradition", label_key="name", desc_key="description",
            data={"slug": row.get("slug"), "region": _clean(row.get("region"))},
            valid_from=row.get("year_founded"),
        )
    for row in tables.get("schools", []):
        add_entity(
            "school", row, etype="School", label_key="name", desc_key="description",
            data={"slug": row.get("slug")}, valid_from=row.get("year_founded"),
        )
    for row in tables.get("lineage_charts", []):
        chart_data: dict[str, Any] = {"slug": row.get("slug")}
        if row.get("tradition_id") is not None:
            chart_data["tradition_id"] = row["tradition_id"]
        if row.get("school_id") is not None:
            chart_data["school_id"] = row["school_id"]
        add_entity(
            "lineagechart",
            row,
            etype="LineageChart",
            label_key="name",
            desc_key="description",
            data=chart_data,
        )
    for row in tables.get("concepts", []):
        add_entity("concept", row, etype="Concept", label_key="name", desc_key="summary",
                   data={"slug": row.get("slug")})
    for row in tables.get("texts", []):
        add_entity(
            "text", row, etype="Text", label_key="title", desc_key="summary",
            data={"slug": row.get("slug"), "text_kind": _clean(row.get("text_kind"))},
            valid_from=row.get("approx_date_start"), valid_to=row.get("approx_date_end"),
        )
    for table, etype, label_key, desc_key in (
        ("practices", "Practice", "name", "summary"),
        ("institutions", "Institution", "name", "summary"),
        ("places", "Place", "name", "summary"),
        ("historical_periods", "Period", "name", "summary"),
        ("events", "Event", "name", "summary"),
    ):
        for row in tables.get(table, []):
            singular = table[:-3] + "y" if table.endswith("ies") else table.rstrip("s")
            add_entity(singular, row, etype=etype, label_key=label_key, desc_key=desc_key,
                       data={"slug": row.get("slug")})

    _add_figures(tables, pool, add_entity)
    _add_transmissions(tables, relationships, emitted)
    _add_lineage_chart_links(tables, relationships, emitted)
    _add_entity_links(tables, relationships, emitted)

    meta = {"adapter": "sacred-lineage", "skipped_rows": skipped}
    return Envelope(
        source_system=SOURCE_SYSTEM,
        generator=generator,
        batch_id=batch_id,
        requires_grounding=False,
        meta=meta,
        sources=pool.sources,
        entities=entities,
        relationships=relationships,
        claims=claims,
    )


def _add_figures(tables, pool, add_entity) -> None:
    for row in tables.get("masters", []):
        citation_ref = pool.default_ref
        source_url = _clean(row.get("source_url"))
        catalog = _clean(row.get("source_catalog"))
        external_ids: list[ExternalIdIn] = []
        ext_slug = _clean(row.get("external_slug"))
        if ext_slug and catalog:
            external_ids.append(ExternalIdIn(authority=catalog, value=ext_slug))
        if source_url:
            citation_ref = pool.ref_for(catalog or source_url, uri=source_url)
        data = {
            "figure_kind": _clean(row.get("figure_kind")),
            "gender": _clean(row.get("gender")),
            "location": _clean(row.get("location")),
            "philosophy_tags": _split_tags(row.get("philosophy_tags")),
            "name_variants": _clean(row.get("name_variants")),
            "source_catalog": catalog,
        }
        add_entity(
            "figure", row, etype="Figure", label_key="name", desc_key="overview",
            data=data, valid_from=row.get("year_born"), valid_to=row.get("year_died"),
            external_ids=external_ids, citation_ref=citation_ref,
        )


def _predicate_lookup(tables) -> dict[int, str]:
    return {rt["id"]: (rt.get("key") or "related_to") for rt in tables.get("relationship_types", [])}


def _add_transmissions(tables, relationships, emitted) -> None:
    predicate_of = _predicate_lookup(tables)
    for row in tables.get("relationships", []):
        subject = _ref("figure", row.get("parent_master_id"))
        obj = _ref("figure", row.get("child_master_id"))
        if subject not in emitted or obj not in emitted:
            continue  # endpoint missing from a partial export; skip rather than fail
        predicate = predicate_of.get(row.get("relationship_type_id"), "transmitted_to")
        data: dict[str, Any] = {}
        if row.get("lineage_id") is not None:
            data["lineage_chart"] = _ref("lineagechart", row["lineage_id"])
        relationships.append(
            RelationshipIn(
                ref=_ref("transmission", row["id"]),
                external_id=_ref("transmission", row["id"]),
                subject=subject,
                predicate=predicate,
                object=obj,
                data=data,
            )
        )


def _add_lineage_chart_links(tables, relationships, emitted) -> None:
    for row in tables.get("lineage_charts", []):
        chart_ref = _ref("lineagechart", row["id"])
        if chart_ref not in emitted:
            continue
        for table, key in (("school", "school_id"), ("tradition", "tradition_id")):
            parent_id = row.get(key)
            if parent_id is None:
                continue
            parent_ref = _ref(table, parent_id)
            if parent_ref not in emitted:
                continue
            relationships.append(
                RelationshipIn(
                    ref=_ref("lineagechartlink", f"{table}:{parent_id}:{row['id']}"),
                    external_id=_ref("lineagechartlink", f"{table}:{parent_id}:{row['id']}"),
                    subject=parent_ref,
                    predicate="has_lineage_chart",
                    object=chart_ref,
                )
            )


def _add_entity_links(tables, relationships, emitted) -> None:
    predicate_of = _predicate_lookup(tables)
    for row in tables.get("entity_links", []):
        s_table = _LINK_TYPE_TO_TABLE.get((row.get("source_type") or "").lower())
        t_table = _LINK_TYPE_TO_TABLE.get((row.get("target_type") or "").lower())
        if not s_table or not t_table:
            continue
        subject = _ref(s_table, row.get("source_id"))
        obj = _ref(t_table, row.get("target_id"))
        if subject not in emitted or obj not in emitted:
            continue
        data = {
            k: _clean(row.get(k))
            for k in ("certainty", "notes", "citation")
            if _clean(row.get(k))
        }
        relationships.append(
            RelationshipIn(
                ref=_ref("entitylink", row["id"]),
                external_id=_ref("entitylink", row["id"]),
                subject=subject,
                predicate=predicate_of.get(row.get("relationship_type_id"), "compared_with"),
                object=obj,
                data=data,
            )
        )

"""Mythographica (Interpretatio-Universalis) source adapter.

Maps the MythGraph ``{ meta, nodes, edges }`` JSON into a Kosmographica contribution
envelope. This is a *federated source import*: the source system is the provenance, and
claims carry citation strings (not AI grounded spans), so the envelope leaves
``requires_grounding=False``.

See `../../../docs/architecture/federation-and-ingestion.md`.
"""

from __future__ import annotations

import re
from typing import Iterable

from ..envelope import ClaimIn, EntityIn, Envelope, RelationshipIn, SourceIn

MODULE = "religion-mythology"
SOURCE_SYSTEM = "mythographica"

# Auto-generated catalog stubs to reject (e.g. "Germanic figure 5", "Germanic
# comparandum 56"). These carry no real content — a templated name/description and
# a generic source — so they are filtered before mapping (see _is_placeholder_node).
_PLACEHOLDER_NAME = re.compile(r"\b(?:figure|comparandum)\s*\d+\b", re.IGNORECASE)


def _is_placeholder_node(node: dict) -> bool:
    """True for empty/partial catalog-filler nodes that should not be ingested."""
    name = (node.get("name") or "").strip()
    if not name:
        return True  # unusable without a label
    if _PLACEHOLDER_NAME.search(name):
        return True
    if "placeholder" in (node.get("description") or "").strip().lower():
        return True
    domains = [str(d).strip().lower() for d in (node.get("domains") or [])]
    if domains == ["catalog"]:
        return True
    return False


def merge_mythgraphs(graphs: Iterable[dict]) -> dict:
    """Merge several MythGraph ``{nodes, edges}`` dicts into one (dedup by id/ref).

    Nodes dedupe on ``id`` and edges on ``id`` (or a composite key), keeping the
    first occurrence. Merging before mapping preserves edges that span source files.
    """
    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}
    for graph in graphs:
        for node in graph.get("nodes", []) or []:
            nid = node.get("id")
            if nid is not None and nid not in nodes:
                nodes[nid] = node
        for edge in graph.get("edges", []) or []:
            key = edge.get("id") or f"e_{edge.get('source')}_{edge.get('target')}_{edge.get('relationType')}"
            if key not in edges:
                edges[key] = edge
    return {
        "meta": {"title": "Mythographica (merged)", "version": "merged"},
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
    }

# Coarse mapping from MythGraph node `type` to a Kosmographica entity type; the original
# value is preserved as `subtype` and in `data.myth_type`.
TYPE_MAP = {
    "deity": "Deity",
    "reconstructed_deity": "Deity",
    "reconstructed": "Deity",
    "primordial": "Primordial",
    "reconstructed_primordial": "Primordial",
    "hero": "Hero",
    "mythic_king": "Hero",
    "sage": "Sage",
    "demon": "Demon",
    "abstract_personification": "Concept",
    "motif": "Motif",
}

# Node confidence labels -> numeric confidence for the description claim.
CONFIDENCE_LEVEL = {"high": 0.9, "medium": 0.65, "low": 0.4, "speculative": 0.2}

# Fields lifted verbatim into Entity.data.
_DATA_FIELDS = (
    "tradition",
    "family",
    "subtradition",
    "region",
    "cultureRegion",
    "period",
    "language",
    "domains",
    "symbols",
    "lineages",
    "originalForm",
    "ontologyClass",
    "alternateNames",
    "roles",
    "realms",
    "motifs",
    "notes",
)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.strip().lower()).strip("_") or "src"


class _SourcePool:
    """Deduplicates citation strings into envelope sources with stable refs."""

    def __init__(self) -> None:
        self._by_citation: dict[str, str] = {}
        self.sources: list[SourceIn] = []

    def ref_for(self, citation: str) -> str:
        citation = citation.strip()
        if citation in self._by_citation:
            return self._by_citation[citation]
        ref = f"src_{_slug(citation)}"
        # Disambiguate rare slug collisions across distinct citations.
        if any(s.ref == ref for s in self.sources):
            ref = f"{ref}_{len(self.sources)}"
        self._by_citation[citation] = ref
        self.sources.append(
            SourceIn(ref=ref, citation=citation, source_system=SOURCE_SYSTEM)
        )
        return ref

    def refs_for(self, citations: list[str] | None) -> list[str]:
        return [self.ref_for(c) for c in (citations or []) if c and c.strip()]


def mythographica_to_envelope(
    graph: dict,
    *,
    generator: str = "mythographica-adapter",
    batch_id: str | None = None,
    drop_placeholders: bool = True,
) -> Envelope:
    """Convert a MythGraph ``{nodes, edges}`` dict into a contribution envelope.

    Empty/partial catalog stubs (``drop_placeholders``, default on) are filtered out
    before mapping, and any edge touching a dropped node is skipped as an orphan.
    """
    pool = _SourcePool()
    entities: list[EntityIn] = []
    relationships: list[RelationshipIn] = []
    claims: list[ClaimIn] = []

    raw_nodes = graph.get("nodes", []) or []
    nodes = [n for n in raw_nodes if not (drop_placeholders and _is_placeholder_node(n))]
    skipped_placeholder = len(raw_nodes) - len(nodes)
    node_ids = {n["id"] for n in nodes}

    for n in nodes:
        raw_type = (n.get("type") or "deity").strip()
        data = {k: n[k] for k in _DATA_FIELDS if n.get(k) not in (None, [], "")}
        data["myth_type"] = raw_type
        if n.get("description"):
            data["description"] = n["description"]
        if n.get("confidenceLevel"):
            data["confidence_level"] = n["confidenceLevel"]

        entities.append(
            EntityIn(
                ref=n["id"],
                external_id=n["id"],
                module=MODULE,
                type=TYPE_MAP.get(raw_type, "Deity"),
                subtype=raw_type,
                label=n["name"],
                data=data,
                valid_from=n.get("attestedFrom"),
                valid_to=n.get("attestedTo"),
            )
        )

        # A node's scholarly description is an assertion about the entity; emit it as a
        # sourced claim so it carries provenance and confidence.
        desc = (n.get("description") or "").strip()
        src_refs = pool.refs_for(n.get("sources"))
        if desc and src_refs:
            claims.append(
                ClaimIn(
                    about=n["id"],
                    about_kind="entity",
                    assertion=desc,
                    confidence=CONFIDENCE_LEVEL.get(n.get("confidenceLevel", ""), 0.5),
                    source_refs=src_refs,
                )
            )

    for e in graph.get("edges", []):
        if e["source"] not in node_ids or e["target"] not in node_ids:
            continue  # orphan edge; skip (validator would otherwise quarantine it)
        rel_ref = e.get("id") or f"e_{e['source']}_{e['target']}_{e['relationType']}"
        relationships.append(
            RelationshipIn(
                ref=rel_ref,
                external_id=e.get("id"),
                subject=e["source"],
                predicate=e["relationType"],
                object=e["target"],
                data={
                    k: e[k]
                    for k in ("label", "directed", "methodology", "notes")
                    if e.get(k) not in (None, [], "")
                },
            )
        )

        explanation = (e.get("explanation") or e.get("label") or "").strip()
        src_refs = pool.refs_for(e.get("sources"))
        if explanation and src_refs:
            conf = e.get("confidence")
            claims.append(
                ClaimIn(
                    about=rel_ref,
                    about_kind="relationship",
                    assertion=explanation,
                    confidence=float(conf) if isinstance(conf, (int, float)) else None,
                    source_refs=src_refs,
                )
            )

    return Envelope(
        source_system=SOURCE_SYSTEM,
        generator=generator,
        batch_id=batch_id,
        requires_grounding=False,
        meta={
            **{k: graph["meta"][k] for k in ("title", "version") if graph.get("meta", {}).get(k)},
            "skipped_placeholder": skipped_placeholder,
        },
        sources=pool.sources,
        entities=entities,
        relationships=relationships,
        claims=claims,
    )

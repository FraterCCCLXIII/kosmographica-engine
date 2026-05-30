"""Mythographica (Interpretatio-Universalis) source adapter.

Maps the MythGraph ``{ meta, nodes, edges }`` JSON into a Kosmographica contribution
envelope. This is a *federated source import*: the source system is the provenance, and
claims carry citation strings (not AI grounded spans), so the envelope leaves
``requires_grounding=False``.

See `../../../docs/architecture/federation-and-ingestion.md`.
"""

from __future__ import annotations

import re

from ..envelope import ClaimIn, EntityIn, Envelope, RelationshipIn, SourceIn

MODULE = "religion-mythology"
SOURCE_SYSTEM = "mythographica"

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
) -> Envelope:
    """Convert a MythGraph ``{nodes, edges}`` dict into a contribution envelope."""
    pool = _SourcePool()
    entities: list[EntityIn] = []
    relationships: list[RelationshipIn] = []
    claims: list[ClaimIn] = []

    node_ids = {n["id"] for n in graph.get("nodes", [])}

    for n in graph.get("nodes", []):
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
        meta={k: graph["meta"][k] for k in ("title", "version") if graph.get("meta", {}).get(k)},
        sources=pool.sources,
        entities=entities,
        relationships=relationships,
        claims=claims,
    )

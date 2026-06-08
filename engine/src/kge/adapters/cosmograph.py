"""Kosmographica cosmograph catalog adapter.

Loads ``catalog.json`` (array of cosmograph records) into a contribution envelope.
Entities only — no claims — so federated import lands as ``machine_validated``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..envelope import EntityIn, Envelope, RelationshipIn, SourceIn

MODULE_PHILOSOPHY = "philosophy-science"
MODULE_RELIGION = "religion-mythology"
SOURCE_SYSTEM = "kosmographica_catalog"
ENTITY_TYPE = "Cosmograph"

# (successor_slug, predecessor_slug) — successor influenced_by predecessor
INFLUENCES: list[tuple[str, str]] = [
    ("world-tree", "three-worlds"),
    ("sumerian-cosmos", "three-worlds"),
    ("babylonian-world-map", "sumerian-cosmos"),
    ("chaldean-cosmology", "babylonian-world-map"),
    ("egyptian-cosmos", "sumerian-cosmos"),
    ("duat-map", "egyptian-cosmos"),
    ("zoroastrian-cosmos", "sumerian-cosmos"),
    ("bundahishn-universe", "zoroastrian-cosmos"),
    ("manichaean-cosmos", "zoroastrian-cosmos"),
    ("vedic-three-worlds", "sumerian-cosmos"),
    ("puranic-universe", "vedic-three-worlds"),
    ("buddhist-meru-cosmos", "puranic-universe"),
    ("jain-lokapurusha", "puranic-universe"),
    ("homeric-cosmos", "vedic-three-worlds"),
    ("hesiodic-cosmos", "homeric-cosmos"),
    ("pythagorean-cosmos", "homeric-cosmos"),
    ("platonic-cosmos", "pythagorean-cosmos"),
    ("aristotelian-cosmos", "platonic-cosmos"),
    ("neoplatonic-cosmos", "platonic-cosmos"),
    ("proclean-cosmos", "neoplatonic-cosmos"),
    ("islamic-falasifa-cosmos", "aristotelian-cosmos"),
    ("islamic-falasifa-cosmos", "neoplatonic-cosmos"),
    ("christian-celestial-hierarchy", "neoplatonic-cosmos"),
    ("great-chain-of-being", "christian-celestial-hierarchy"),
    ("kabbalistic-tree", "sefer-yetzirah-cosmos"),
    ("merkabah-cosmos", "kabbalistic-tree"),
    ("gnostic-pleroma", "platonic-cosmos"),
    ("hermetic-cosmos", "platonic-cosmos"),
    ("akbarian-cosmos", "neoplatonic-cosmos"),
    ("illuminationist-cosmos", "akbarian-cosmos"),
    ("mappa-mundi", "great-chain-of-being"),
    ("dantean-cosmos", "mappa-mundi"),
    ("copernican-cosmos", "aristotelian-cosmos"),
    ("keplerian-cosmos", "copernican-cosmos"),
    ("newtonian-universe", "copernican-cosmos"),
    ("darwinian-tree", "linnaean-taxonomy"),
    ("relativistic-cosmos", "newtonian-universe"),
    ("big-bang-universe", "relativistic-cosmos"),
    ("inflationary-universe", "big-bang-universe"),
    ("spiral-dynamics", "graves-emergent-cycles"),
    ("aqal", "spiral-dynamics"),
    ("kohlberg-development", "piaget-development"),
    ("kegan-orders", "loevinger-ego-development"),
    ("yggdrasil", "world-tree"),
    ("huayan-indras-net", "buddhist-meru-cosmos"),
    ("huayan-cosmos", "huayan-indras-net"),
    ("kalachakra-mandala", "buddhist-meru-cosmos"),
    ("popol-vuh-cosmos", "maya-world-tree"),
    ("inca-three-worlds", "andean-chakana"),
    ("kongo-cosmogram", "three-worlds"),
    ("whitehead-process-cosmos", "bergson-evolutionary-cosmos"),
    ("teilhard-noosphere", "whitehead-process-cosmos"),
    ("gebser-structures-of-consciousness", "teilhard-noosphere"),
    ("network-science", "cybernetics"),
    ("agentic-cosmology", "foundation-model-world-models"),
    ("foundation-model-world-models", "embedding-space-cosmology"),
    ("wikidata", "semantic-web"),
    ("openalex", "wikidata"),
]


def slugify(label: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
    return s or "cosmograph"


def _default_module(tradition: str, typ: str) -> str:
    t = tradition.lower()
    typ_l = typ.lower()
    if typ_l in {"scientific", "psychological", "developmental", "systems", "integral", "cognitive", "information", "knowledge", "classification", "evolutionary", "complexity", "consciousness", "sociology", "ecological", "philosophical"}:
        return MODULE_PHILOSOPHY
    if any(
        k in t
        for k in (
            "paleolithic",
            "neolithic",
            "proto-indo",
            "indigenous",
            "diné",
            "lakota",
            "hopi",
            "iroquois",
            "anishinaabe",
            "inuit",
            "maya",
            "aztec",
            "mixtec",
            "toltec",
            "teotihuacan",
            "inca",
            "andean",
            "muisca",
            "tupi",
            "mapuche",
            "amazonian",
            "yoruba",
            "kongo",
            "dogon",
            "akan",
            "dinka",
            "zulu",
            "nubian",
            "berber",
            "amazigh",
            "norse",
            "ossetian",
            "sámi",
            "sami",
            "turkic",
            "mongolian",
            "finno-ugric",
            "shaman",
            "siberian",
        )
    ):
        return MODULE_RELIGION
    if typ_l in {"mythic", "mystical", "esoteric", "narrative cosmograph", "topological"} and typ_l != "scientific":
        if typ_l in {"mystical", "esoteric", "mythic"}:
            return MODULE_RELIGION
    return MODULE_PHILOSOPHY


def cosmograph_to_envelope(
    source: str | Path | list[dict], *, batch_id: str | None = None
) -> Envelope:
    if isinstance(source, list):
        records = source
    else:
        records = json.loads(Path(source).read_text(encoding="utf-8"))
    slug_to_ref: dict[str, str] = {}
    entities: list[EntityIn] = []
    sources: list[SourceIn] = []
    source_keys: set[str] = set()

    for i, row in enumerate(records):
        label = row["cosmograph"].strip()
        slug = slugify(label)
        ref = f"cg{i}"
        slug_to_ref[slug] = ref

        tradition = row.get("tradition", "").strip()
        typ = row.get("type", "").strip()
        module = row.get("module", "").strip() or _default_module(tradition, typ)
        primary = row.get("primary_sources", "").strip()

        if primary and primary not in source_keys:
            source_keys.add(primary)
            sources.append(
                SourceIn(ref=f"src:{len(sources)}", citation=primary, uri=None)
            )

        data = {
            "description": row.get("description", "").strip(),
            "importance": row.get("importance", "").strip(),
            "tradition": tradition,
            "region": row.get("region", "").strip(),
            "date_range": row.get("dates", "").strip(),
            "cosmograph_type": typ,
            "domain": row.get("domain", "").strip(),
            "topology": row.get("topology", "").strip(),
            "human_position": row.get("human_position", "").strip(),
            "liberation_path": row.get("liberation_path", "").strip(),
            "primary_sources": primary,
            "thumbnail_url": row.get("thumbnail_url", "").strip(),
            "image_url": row.get("image_url", "").strip(),
            "image_title": row.get("image_title", "").strip(),
            "image_source": row.get("image_source", "").strip(),
            "image_license": row.get("image_license", "").strip(),
            "image_page_url": row.get("image_page_url", "").strip(),
        }
        # Drop empty strings from data
        data = {k: v for k, v in data.items() if v}

        entities.append(
            EntityIn(
                ref=ref,
                module=module,
                type=ENTITY_TYPE,
                label=label,
                external_id=f"cosmo:{slug}",
                data=data,
                valid_from=row.get("valid_from"),
                valid_to=row.get("valid_to"),
            )
        )

    relationships: list[RelationshipIn] = []
    for j, (succ, pred) in enumerate(INFLUENCES):
        s_ref = slug_to_ref.get(succ)
        p_ref = slug_to_ref.get(pred)
        if s_ref and p_ref:
            relationships.append(
                RelationshipIn(
                    ref=f"rel{j}",
                    subject=s_ref,
                    predicate="influenced_by",
                    object=p_ref,
                    data={"note": "catalog lineage edge"},
                )
            )

    return Envelope(
        source_system=SOURCE_SYSTEM,
        generator="human:catalog-curator",
        batch_id=batch_id,
        requires_grounding=False,
        sources=sources,
        entities=entities,
        relationships=relationships,
        claims=[],
    )

"""Controlled entity-type vocabulary and source classification (governance).

This is the single source of truth for "what canonical type/subtype/status does a raw
source node map to?". Both the ingest adapters and the reclassification job depend on it,
so mapping decisions live in exactly one place.

Two governance principles drive the design:

* **No silent fallback.** Unmapped source ``type`` values are *not* coerced to ``Deity``.
  They keep a best-guess type but are flagged ``needs_review`` so a human resolves them —
  this is the discipline that the flat/mis-typed corpus was missing.
* **Historicity is a facet, not a type.** A figure's status (historical / legendary /
  mythic / reconstructed) is orthogonal to whether it is a Deity/Sage/Hero, so it is a
  separate ``status`` facet rather than baked into the type or subtype.
* **Collectives are subtypes, not types.** Pantheons, pairs, and deity classes stay
  ``Deity`` / ``Hero`` (etc.) with collective ``subtype`` and ``data.is_collective``;
  source ``ontologyClass: group`` is a facet, never a destination entity type.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# --- Canonical entity types (controlled vocabulary) -------------------------------------

DEITY = "Deity"
PRIMORDIAL = "Primordial"
DEMON = "Demon"
HERO = "Hero"
SAGE = "Sage"
FIGURE = "Figure"
CONCEPT = "Concept"
MOTIF = "Motif"
TRADITION = "Tradition"
SCHOOL = "School"
LINEAGE_CHART = "LineageChart"
TEXT = "Text"

CANONICAL_ENTITY_TYPES = frozenset(
    {
        DEITY,
        PRIMORDIAL,
        DEMON,
        HERO,
        SAGE,
        FIGURE,
        CONCEPT,
        MOTIF,
        TRADITION,
        SCHOOL,
        LINEAGE_CHART,
        TEXT,
    }
)

# --- Historicity / status facet (stored at ``data.status``) -----------------------------

STATUS_HISTORICAL = "historical"
STATUS_LEGENDARY = "legendary"
STATUS_MYTHIC = "mythic"
STATUS_RECONSTRUCTED = "reconstructed"
STATUS_UNKNOWN = "unknown"

CANONICAL_STATUSES = frozenset(
    {STATUS_HISTORICAL, STATUS_LEGENDARY, STATUS_MYTHIC, STATUS_RECONSTRUCTED, STATUS_UNKNOWN}
)

# Status is only meaningful for person/being types. Abstract types (Concept, Motif,
# Tradition, ...) carry no historicity facet.
_STATUS_BEARING_TYPES = frozenset({DEITY, PRIMORDIAL, DEMON, HERO, SAGE, FIGURE})

# --- Source mapping tables --------------------------------------------------------------

# MythGraph node ``type`` -> canonical entity type. Explicit and exhaustive over the
# values observed in the corpus; anything not here is flagged for review (see ``classify``).
MYTH_TYPE_TO_ENTITY: dict[str, str] = {
    # divine
    "deity": DEITY,
    "reconstructed_deity": DEITY,
    "reconstructed": DEITY,
    "yazata": DEITY,
    "mystery_cult_deity": DEITY,
    "deity_group": DEITY,
    "deity_pair": DEITY,
    "deity_class": DEITY,
    # primordial / cosmogonic
    "primordial": PRIMORDIAL,
    "reconstructed_primordial": PRIMORDIAL,
    "primordial_deity": PRIMORDIAL,
    "primordial_cosmic_being": PRIMORDIAL,
    "primordial_giant": PRIMORDIAL,
    "titan": PRIMORDIAL,
    # malevolent / liminal
    "demon": DEMON,
    "anti_deity": DEMON,
    "monster": DEMON,
    "serpent_monster": DEMON,
    "chaos_serpent": DEMON,
    # heroes / quasi-historical rulers
    "hero": HERO,
    "mythic_king": HERO,
    "hero_deity": HERO,
    "hero_pair": HERO,
    # wisdom figures
    "sage": SAGE,
    "sage_divine_messenger": SAGE,
    # abstractions
    "abstract_personification": CONCEPT,
    "reconstructed_concept": CONCEPT,
    "motif": MOTIF,
}

# Explicit collective source types (canonical type is Deity/Hero; collective via subtype).
_COLLECTIVE_MYTH_TYPES = frozenset(
    {"deity_group", "deity_pair", "deity_class", "hero_pair", "reconstructed_deity_pair"}
)

# Genuinely ambiguous source types: we keep a best-guess type but flag for human review
# rather than guessing silently.
AMBIGUOUS_MYTH_TYPES: dict[str, str] = {
    "ancestor_lawgiver": HERO,
    "reconstructed_ancestor": HERO,
    "reconstructed_myth": MOTIF,
}

# ``ontologyClass`` values that *decide* the entity type (overrides the raw ``type``).
# Note: ``group`` is intentionally absent — it marks a collective *facet*, not a type.
ONTOLOGY_CLASS_TO_ENTITY: dict[str, str] = {
    "comparative_motif": MOTIF,
    "cosmic_principle": CONCEPT,
}

# ``ontologyClass`` that pins historicity regardless of the mythic default.
ONTOLOGY_CLASS_STATUS: dict[str, str] = {
    "historical_master": STATUS_HISTORICAL,
    "tulku": STATUS_HISTORICAL,
}

_RECONSTRUCTED_PREFIX = "reconstructed"
_LEGENDARY_TYPES = frozenset({"hero", "mythic_king", "hero_deity", "ancestor_lawgiver"})

# Structural collective marker in the *source type* itself (e.g. ``deity_pair``,
# ``reconstructed_deity_pair``, ``hero_group``).
_COLLECTIVE_TYPE = re.compile(r"(?:^|_)(pair|group|class|triad|pantheon|twins?)(?:_|$)", re.IGNORECASE)

# Name heuristic for collectives mis-typed as individuals (e.g. an "abstract_personification"
# actually naming a pantheon/triad/class of deities, or a "deity" named "Dragon Kings").
_COLLECTIVE_NAME = re.compile(
    r"\b(?:"
    r"pantheon|triad|trinity|ennead|dodekatheon|tetrad|dyad|"
    r"deities|gods|goddesses|spirits|"
    r"adityas|asuras|maruts|rudras|vasus|vishvedevas|"
    r"archons|aeons|amesha\s+spentas|"
    r"valkyries|norns|moirai|muses|graces|charites|gorgons|"
    r"titans|olympians|aesir|vanir|anunnaki|igigi"
    r")\b"
    r"|^(?:two|three|four|five|six|seven|eight|nine|ten|twelve|thirty-three)\b"
    r"|\b(?:twins|kings|queens|sisters|brothers|mothers|fathers|lords|ladies|"
    r"suns|mountains|maidens|sages|rishis|guardians|protectors)\s*$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Classification:
    """The canonical typing decision for one source node."""

    entity_type: str
    subtype: str | None
    status: str | None
    is_collective: bool = False
    needs_review: bool = False
    review_reason: str | None = None


def _collective_base_type(raw_type: str) -> str:
    """Deity vs Hero for a source type that structurally names a collective."""
    return HERO if "hero" in raw_type else DEITY


def _derive_status(raw_type: str, ontology_class: str, entity_type: str) -> str | None:
    if entity_type not in _STATUS_BEARING_TYPES:
        return None
    if ontology_class in ONTOLOGY_CLASS_STATUS:
        return ONTOLOGY_CLASS_STATUS[ontology_class]
    if raw_type.startswith(_RECONSTRUCTED_PREFIX):
        return STATUS_RECONSTRUCTED
    if raw_type in _LEGENDARY_TYPES or entity_type == HERO:
        return STATUS_LEGENDARY
    if entity_type in {DEITY, PRIMORDIAL, DEMON}:
        return STATUS_MYTHIC
    return STATUS_UNKNOWN


def apply_classification_data(data: dict, cls: Classification) -> dict:
    """Merge classification facets into an entity ``data`` dict (ingest + reclassify)."""
    out = dict(data)
    if cls.status:
        out["status"] = cls.status
    else:
        out.pop("status", None)
    if cls.is_collective:
        out["is_collective"] = True
    else:
        out.pop("is_collective", None)
    if cls.needs_review:
        out["needs_taxonomy_review"] = True
        if cls.review_reason:
            out["taxonomy_review_reason"] = cls.review_reason
    else:
        out.pop("needs_taxonomy_review", None)
        out.pop("taxonomy_review_reason", None)
    return out


def classify(
    *, myth_type: str | None, ontology_class: str | None = None, label: str = ""
) -> Classification:
    """Map a raw source node to a canonical (type, subtype, status) with review flags.

    Resolution order: ``ontologyClass`` type override -> explicit ``type`` map -> structural
    collective marker -> ambiguous map (flagged) -> unmapped (best-guess Deity, flagged).
    ``ontologyClass: group`` and collective-name heuristics refine CONCEPT -> Deity and set
    ``is_collective``; they never mint a meta-type.
    """
    raw = (myth_type or "").strip().lower()
    oc = (ontology_class or "").strip().lower()
    name = label or ""

    needs_review = False
    review_reason: str | None = None
    is_collective = raw in _COLLECTIVE_MYTH_TYPES or bool(_COLLECTIVE_TYPE.search(raw))

    if oc in ONTOLOGY_CLASS_TO_ENTITY:
        entity_type = ONTOLOGY_CLASS_TO_ENTITY[oc]
    elif _COLLECTIVE_TYPE.search(raw):
        entity_type = _collective_base_type(raw)
    elif raw in MYTH_TYPE_TO_ENTITY:
        entity_type = MYTH_TYPE_TO_ENTITY[raw]
    elif raw in AMBIGUOUS_MYTH_TYPES:
        entity_type = AMBIGUOUS_MYTH_TYPES[raw]
        needs_review = True
        review_reason = f"ambiguous source type {raw!r}"
    else:
        entity_type = DEITY
        needs_review = True
        review_reason = f"unmapped source type {raw!r}" if raw else "missing source type"

    # ontologyClass "group" = collective of beings (facet), not a separate entity type.
    if oc == "group":
        is_collective = True
        if entity_type == CONCEPT:
            entity_type = DEITY
            needs_review = True
            review_reason = "ontologyClass group: collective of beings, not abstract concept"

    # Name heuristic: mis-typed individual labels that name a collective.
    if _COLLECTIVE_NAME.search(name):
        is_collective = True
        explicit_collective = raw in _COLLECTIVE_MYTH_TYPES or bool(_COLLECTIVE_TYPE.search(raw))
        if entity_type == CONCEPT:
            entity_type = DEITY
            needs_review = True
            review_reason = "name suggests a collective of beings"
        elif (
            entity_type in {DEITY, PRIMORDIAL, HERO}
            and not needs_review
            and not explicit_collective
        ):
            needs_review = True
            review_reason = "name suggests a collective of beings"

    status = _derive_status(raw, oc, entity_type)
    return Classification(
        entity_type=entity_type,
        subtype=myth_type or None,
        status=status,
        is_collective=is_collective,
        needs_review=needs_review,
        review_reason=review_reason,
    )

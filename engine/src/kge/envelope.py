"""The contribution envelope — the single write format for the engine (ADR-010).

Every write to the canonical store (human, adapter, or AI) arrives as one of these and
passes the staging gate. Within an envelope, records are wired together by local
``ref`` strings; real KIDs are minted at load time.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

SCHEMA_VERSION = "1.0"


class SourceIn(BaseModel):
    ref: str = Field(description="Local ref, unique within the envelope.")
    citation: str
    uri: str | None = None
    external_id: str | None = None
    data: dict = Field(default_factory=dict)


class SupportSpan(BaseModel):
    """Exact supporting text from a cited source (grounded generation, ADR-013)."""

    source_ref: str
    quote: str
    locator: str | None = None  # page / line / url fragment


class ExternalIdIn(BaseModel):
    authority: str  # e.g. wikidata, viaf, pleiades
    value: str


class EntityIn(BaseModel):
    ref: str
    module: str
    type: str
    label: str
    subtype: str | None = None
    external_id: str | None = None
    data: dict = Field(default_factory=dict)
    valid_from: int | None = None
    valid_to: int | None = None
    sensitivity: str = "public"
    external_ids: list[ExternalIdIn] = Field(default_factory=list)


class RelationshipIn(BaseModel):
    ref: str
    subject: str  # local ref or existing KID
    predicate: str
    object: str  # local ref or existing KID
    external_id: str | None = None
    data: dict = Field(default_factory=dict)


class ClaimIn(BaseModel):
    about: str  # local ref or existing KID
    assertion: str
    about_kind: str = "entity"  # entity | relationship
    confidence: float | None = None  # often set by the verifier, not the author
    source_refs: list[str] = Field(default_factory=list)
    support_spans: list[SupportSpan] = Field(default_factory=list)
    sensitivity: str = "public"


class Envelope(BaseModel):
    schema_version: str = SCHEMA_VERSION
    source_system: str
    generator: str | None = None
    batch_id: str | None = None
    meta: dict = Field(default_factory=dict)

    # Grounded-generation mode (ADR-013). When True (AI authoring), every claim MUST
    # carry a non-empty support span quoting its source, or it is quarantined. Federated
    # source imports leave this False: claims are sourced (citations) but not span-grounded,
    # so missing spans are warnings, not errors.
    requires_grounding: bool = False

    sources: list[SourceIn] = Field(default_factory=list)
    entities: list[EntityIn] = Field(default_factory=list)
    relationships: list[RelationshipIn] = Field(default_factory=list)
    claims: list[ClaimIn] = Field(default_factory=list)

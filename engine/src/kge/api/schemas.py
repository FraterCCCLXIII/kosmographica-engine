"""Response models for the read API (kept separate from the write-side envelope)."""

from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, ConfigDict


class SourceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    citation: str
    uri: str | None = None


class ClaimOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    about_kind: str
    about_id: str
    assertion: str
    confidence: float
    tier: str
    generator: str | None = None
    batch_id: str | None = None
    disputed: bool
    support_spans: list = []
    sources: list[SourceOut] = []
    recorded_at: dt.datetime


class EntityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    module: str
    type: str
    subtype: str | None = None
    label: str
    data: dict = {}
    valid_from: int | None = None
    valid_to: int | None = None
    tier: str
    generator: str | None = None
    sensitivity: str
    recorded_at: dt.datetime


class RelationshipOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    subject_id: str
    predicate: str
    object_id: str
    data: dict = {}
    tier: str


class EntityDetailOut(EntityOut):
    claims: list[ClaimOut] = []


class GraphOut(BaseModel):
    nodes: list[EntityOut]
    edges: list[RelationshipOut]


class VerificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    verifier: str
    support_label: str
    support_score: float
    outcome: str
    reason: str
    created_at: dt.datetime


class ClaimAuditOut(ClaimOut):
    """A claim plus the human-readable label of what it is about (for the console)."""

    about_label: str | None = None
    verifications: list[VerificationOut] = []


class AuditStats(BaseModel):
    claims_by_tier: dict[str, int]
    entities_by_tier: dict[str, int]
    claims_by_generator: list[dict]
    disputes: int


class SearchHitOut(BaseModel):
    entity: EntityOut
    rank: float


class Page(BaseModel):
    items: list
    total: int
    limit: int
    offset: int

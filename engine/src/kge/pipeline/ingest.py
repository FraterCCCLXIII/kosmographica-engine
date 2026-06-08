"""Ingestion pipeline: stage -> validate -> reconcile -> load -> index.

The single write path for the canonical store (ADR-010). Every contribution envelope
runs through here. On validation failure the batch is *quarantined* (not loaded, not
silently dropped — ADR-011); the caller inspects the returned report.

Reconciliation in v1 is deterministic only (entity-resolution.md): identity is matched
by ``(source_system, external_id)``. No cross-source / name-only auto-merge.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..envelope import ClaimIn, Envelope
from ..ids import uuid7
from ..models import Claim, Entity, ExternalId, Relationship, Source, TrustTier
from ..validation import ValidationReport, validate_envelope


@dataclass
class IngestResult:
    batch_id: str
    report: ValidationReport
    quarantined: bool = False
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.quarantined


def _default_tier(env: Envelope) -> str:
    # AI-authored (grounded) writes land unverified until the verifier runs; curated
    # federated source imports are public-but-badged from the start.
    return TrustTier.MACHINE_UNVERIFIED if env.requires_grounding else TrustTier.MACHINE_VALIDATED


def ingest(session: Session, env: Envelope, *, tier: str | None = None) -> IngestResult:
    batch_id = env.batch_id or uuid7().hex
    report = validate_envelope(env)
    if not report.ok:
        return IngestResult(batch_id=batch_id, report=report, quarantined=True)

    tier = tier or _default_tier(env)
    counts = {
        "sources_created": 0,
        "entities_created": 0,
        "entities_matched": 0,
        "entities_updated": 0,
        "relationships_created": 0,
        "relationships_matched": 0,
        "claims_created": 0,
        "claims_skipped": 0,
    }

    src_kid = _load_sources(session, env, counts)
    ent_kid = _load_entities(session, env, tier, batch_id, counts)
    rel_kid = _load_relationships(session, env, tier, batch_id, ent_kid, counts)
    _load_claims(session, env, tier, batch_id, ent_kid, rel_kid, src_kid, counts)

    session.flush()
    return IngestResult(batch_id=batch_id, report=report, counts=counts)


def _load_sources(session: Session, env: Envelope, counts: dict[str, int]) -> dict[str, str]:
    ref_to_kid: dict[str, str] = {}
    for s in env.sources:
        existing = session.scalar(
            select(Source).where(
                Source.source_system == env.source_system, Source.citation == s.citation
            )
        )
        if existing:
            ref_to_kid[s.ref] = existing.id
            continue
        src = Source(
            citation=s.citation,
            uri=s.uri,
            source_system=env.source_system,
            external_id=s.external_id,
            data=s.data,
        )
        session.add(src)
        session.flush()
        ref_to_kid[s.ref] = src.id
        counts["sources_created"] += 1
    return ref_to_kid


def _load_entities(
    session: Session, env: Envelope, tier: str, batch_id: str, counts: dict[str, int]
) -> dict[str, str]:
    ref_to_kid: dict[str, str] = {}
    for e in env.entities:
        existing = None
        if e.external_id:
            existing = session.scalar(
                select(Entity).where(
                    Entity.source_system == env.source_system,
                    Entity.external_id == e.external_id,
                )
            )
        if existing:
            if e.data:
                merged = dict(existing.data or {})
                merged.update(e.data)
                existing.data = merged
                counts["entities_updated"] = counts.get("entities_updated", 0) + 1
            ref_to_kid[e.ref] = existing.id
            counts["entities_matched"] += 1
            continue
        ent = Entity(
            module=e.module,
            type=e.type,
            subtype=e.subtype,
            label=e.label,
            data=e.data,
            valid_from=e.valid_from,
            valid_to=e.valid_to,
            source_system=env.source_system,
            external_id=e.external_id,
            tier=tier,
            generator=env.generator,
            batch_id=batch_id,
            sensitivity=e.sensitivity,
        )
        session.add(ent)
        session.flush()
        ref_to_kid[e.ref] = ent.id
        counts["entities_created"] += 1
        for x in e.external_ids:
            session.add(ExternalId(kid=ent.id, authority=x.authority, value=x.value))
    return ref_to_kid


def _resolve(ref: str, ref_to_kid: dict[str, str]) -> str | None:
    return ref if ref.startswith("kg:") else ref_to_kid.get(ref)


def _load_relationships(
    session: Session,
    env: Envelope,
    tier: str,
    batch_id: str,
    ent_kid: dict[str, str],
    counts: dict[str, int],
) -> dict[str, str]:
    ref_to_kid: dict[str, str] = {}
    for r in env.relationships:
        subject = _resolve(r.subject, ent_kid)
        obj = _resolve(r.object, ent_kid)
        if subject is None or obj is None:
            continue  # already reported by the validator; defensive
        existing = None
        if r.external_id:
            existing = session.scalar(
                select(Relationship).where(
                    Relationship.source_system == env.source_system,
                    Relationship.external_id == r.external_id,
                )
            )
        if existing:
            ref_to_kid[r.ref] = existing.id
            counts["relationships_matched"] += 1
            continue
        rel = Relationship(
            subject_id=subject,
            predicate=r.predicate,
            object_id=obj,
            data=r.data,
            source_system=env.source_system,
            external_id=r.external_id,
            tier=tier,
            generator=env.generator,
            batch_id=batch_id,
        )
        session.add(rel)
        session.flush()
        ref_to_kid[r.ref] = rel.id
        counts["relationships_created"] += 1
    return ref_to_kid


def _resolve_about(c: ClaimIn, ent_kid: dict[str, str], rel_kid: dict[str, str]) -> str | None:
    if c.about.startswith("kg:"):
        return c.about
    return rel_kid.get(c.about) if c.about_kind == "relationship" else ent_kid.get(c.about)


def _load_claims(
    session: Session,
    env: Envelope,
    tier: str,
    batch_id: str,
    ent_kid: dict[str, str],
    rel_kid: dict[str, str],
    src_kid: dict[str, str],
    counts: dict[str, int],
) -> None:
    for c in env.claims:
        about_id = _resolve_about(c, ent_kid, rel_kid)
        if about_id is None:
            continue
        # Idempotent re-runs: don't duplicate an identical claim from the same generator.
        duplicate = session.scalar(
            select(Claim.id).where(
                Claim.about_id == about_id,
                Claim.assertion == c.assertion,
                Claim.generator == env.generator,
            )
        )
        if duplicate:
            counts["claims_skipped"] += 1
            continue
        claim = Claim(
            about_kind=c.about_kind,
            about_id=about_id,
            assertion=c.assertion,
            confidence=c.confidence if c.confidence is not None else 0.0,
            support_spans=[span.model_dump() for span in c.support_spans],
            tier=tier,
            generator=env.generator,
            batch_id=batch_id,
            sensitivity=c.sensitivity,
        )
        for sref in c.source_refs:
            sid = src_kid.get(sref)
            if sid:
                claim.sources.append(session.get(Source, sid))
        session.add(claim)
        counts["claims_created"] += 1

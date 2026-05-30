"""Source parity / convergence check (migration-and-convergence.md).

Parity here is **consistency, not completeness** — a known-incomplete source (e.g.
Sacred-Lineage) is expected to have partial coverage. The check confirms a source's
records loaded coherently: every entity is addressable by its ``(source_system,
external_id)`` key (the idempotency contract) and the source actually produced rows.
A source is "converged" when it has entities and all of them carry an external_id.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import Claim, Entity, Relationship


def source_parity(session: Session, source_system: str) -> dict:
    entities = session.scalar(
        select(func.count()).select_from(Entity).where(Entity.source_system == source_system)
    ) or 0
    relationships = session.scalar(
        select(func.count()).select_from(Relationship).where(
            Relationship.source_system == source_system
        )
    ) or 0
    claims = session.scalar(
        select(func.count()).select_from(Claim).where(Claim.generator.like(f"%{source_system}%"))
    ) or 0
    missing_xid = session.scalar(
        select(func.count()).select_from(Entity).where(
            Entity.source_system == source_system, Entity.external_id.is_(None)
        )
    ) or 0
    return {
        "source_system": source_system,
        "entities": entities,
        "relationships": relationships,
        "claims": claims,
        "entities_missing_external_id": missing_xid,
        # Idempotency contract holds (every entity keyed) and the source produced rows.
        "converged": entities > 0 and missing_xid == 0,
    }

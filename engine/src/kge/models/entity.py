"""The generic Entity table (ADR-007): one polymorphic node table, no per-type tables."""

from __future__ import annotations

from sqlalchemy import Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..ids import entity_kid
from .base import Base, ProvenanceMixin


class Entity(Base, ProvenanceMixin):
    __tablename__ = "entities"

    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=entity_kid)

    module: Mapped[str] = mapped_column(String(64), index=True)
    type: Mapped[str] = mapped_column(String(64), index=True)
    subtype: Mapped[str | None] = mapped_column(String(64))
    label: Mapped[str] = mapped_column(String(512), index=True)

    # Type-specific fields live in JSONB rather than dedicated columns.
    data: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Valid-time anchors (the *world* time the entity existed), as signed years.
    # Bitemporal pairing with ``recorded_at`` (transaction time) from the mixin.
    valid_from: Mapped[int | None] = mapped_column(Integer)
    valid_to: Mapped[int | None] = mapped_column(Integer)

    __table_args__ = (
        # One canonical record per (source_system, external_id) for idempotent upserts.
        UniqueConstraint(
            "source_system", "external_id", name="uq_entity_source_external"
        ),
        Index("ix_entity_module_type", "module", "type"),
    )

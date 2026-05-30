"""Typed relationships (edges) between entities."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..ids import relationship_kid
from .base import Base, ProvenanceMixin


class Relationship(Base, ProvenanceMixin):
    __tablename__ = "relationships"

    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=relationship_kid)

    subject_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )
    predicate: Mapped[str] = mapped_column(String(128), index=True)
    object_id: Mapped[str] = mapped_column(
        ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )

    data: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (
        UniqueConstraint(
            "source_system", "external_id", name="uq_relationship_source_external"
        ),
        Index("ix_relationship_triple", "subject_id", "predicate", "object_id"),
    )

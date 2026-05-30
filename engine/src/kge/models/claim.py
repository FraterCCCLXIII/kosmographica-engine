"""Claims: provenance-tagged, confidence-scored assertions about entities/relationships.

Claims are the atomic unit of trust. A contradicting claim opens a dispute; both
coexist with provenance (ADR-013, no AI edit wars).
"""

from __future__ import annotations

from sqlalchemy import Boolean, Float, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..ids import claim_kid
from .base import Base, ProvenanceMixin
from .source import Source, claim_sources


class Claim(Base, ProvenanceMixin):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=claim_kid)

    # Polymorphic subject: the KID this claim is about (entity or relationship).
    about_kind: Mapped[str] = mapped_column(String(16), index=True)
    about_id: Mapped[str] = mapped_column(String(80), index=True)

    assertion: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, index=True)

    # Grounded-generation evidence: exact supporting span(s) from the cited source(s).
    support_spans: Mapped[list] = mapped_column(JSONB, default=list)

    disputed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    sources: Mapped[list[Source]] = relationship(secondary=claim_sources, lazy="selectin")

    __table_args__ = (Index("ix_claim_about", "about_kind", "about_id"),)

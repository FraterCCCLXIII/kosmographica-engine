"""Sources / references that back claims."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..ids import source_kid
from .base import Base

# Many-to-many: a claim may cite several sources; a source may back many claims.
claim_sources = Table(
    "claim_sources",
    Base.metadata,
    Column("claim_id", ForeignKey("claims.id", ondelete="CASCADE"), primary_key=True),
    Column("source_id", ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True),
)


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=source_kid)

    citation: Mapped[str] = mapped_column(String(2048))
    uri: Mapped[str | None] = mapped_column(String(2048), index=True)
    source_system: Mapped[str | None] = mapped_column(String(64), index=True)
    external_id: Mapped[str | None] = mapped_column(String(256))

    data: Mapped[dict] = mapped_column(JSONB, default=dict)

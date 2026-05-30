"""Cross-source ``sameAs`` proposals (entity-resolution.md).

Reconciliation is **non-destructive**: a row records a *proposal* that two entities
from different sources are the same. Identity is a mapping, never an overwrite.
Deterministic (shared external-ID) matches are auto-accepted; scored name matches
land in the review queue. Rejections are remembered so a pair is not re-proposed.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, Float, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Reconciliation(Base):
    __tablename__ = "reconciliations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Canonical ordering (left < right) so a pair is stored once.
    left_kid: Mapped[str] = mapped_column(String(80), index=True)
    right_kid: Mapped[str] = mapped_column(String(80), index=True)
    left_source: Mapped[str | None] = mapped_column(String(64))
    right_source: Mapped[str | None] = mapped_column(String(64))

    match_method: Mapped[str] = mapped_column(String(32))  # deterministic | scored | manual
    score: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(16), default="proposed", index=True)  # proposed|accepted|rejected
    reason: Mapped[str | None] = mapped_column(String(512))

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    decided_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("left_kid", "right_kid", name="uq_reconciliation_pair"),
    )

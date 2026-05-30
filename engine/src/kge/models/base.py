"""Declarative base and shared mixins."""

from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ..models.enums import Sensitivity, TrustTier


class Base(DeclarativeBase):
    pass


class ProvenanceMixin:
    """Columns every canonical record carries (ADR-013).

    Records are append-only and bitemporal: ``recorded_at`` is transaction time;
    a write *supersedes* a prior record (it never overwrites in place), so the full
    history — and thus every AI write — stays auditable and reversible.
    """

    tier: Mapped[str] = mapped_column(
        String(32), default=TrustTier.MACHINE_UNVERIFIED, index=True
    )
    generator: Mapped[str | None] = mapped_column(String(128), index=True)
    batch_id: Mapped[str | None] = mapped_column(String(64), index=True)
    sensitivity: Mapped[str] = mapped_column(String(16), default=Sensitivity.PUBLIC)

    source_system: Mapped[str | None] = mapped_column(String(64), index=True)
    external_id: Mapped[str | None] = mapped_column(String(256))

    recorded_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    superseded_by: Mapped[str | None] = mapped_column(String(80), index=True)

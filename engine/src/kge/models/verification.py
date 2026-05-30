"""Verification records — the verifier's audit trail for AI-authored claims (ADR-013).

Every verifier run is stored so that auditing is a query: the support score that gated a
claim, which model produced it, and why it was accepted / rejected / disputed.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Verification(Base):
    __tablename__ = "verifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    claim_id: Mapped[str] = mapped_column(
        ForeignKey("claims.id", ondelete="CASCADE"), index=True
    )
    verifier: Mapped[str] = mapped_column(String(128), index=True)

    # entailed | not_entailed | fabricated
    support_label: Mapped[str] = mapped_column(String(32), index=True)
    support_score: Mapped[float] = mapped_column(Float)

    # accept | reject | dispute
    outcome: Mapped[str] = mapped_column(String(16), index=True)
    reason: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

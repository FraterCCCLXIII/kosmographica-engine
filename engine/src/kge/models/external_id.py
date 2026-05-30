"""External identifier links (sameAs): KID <-> authority identifier.

Backs deterministic reconciliation (entity-resolution.md) and external linking
(identifiers-and-versioning.md).
"""

from __future__ import annotations

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ExternalId(Base):
    __tablename__ = "external_ids"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    kid: Mapped[str] = mapped_column(String(80), index=True)
    authority: Mapped[str] = mapped_column(String(64), index=True)  # e.g. wikidata, viaf
    value: Mapped[str] = mapped_column(String(256), index=True)

    __table_args__ = (
        # An external authority id may be claimed by entities from multiple sources —
        # that shared (authority, value) is the deterministic sameAs signal the
        # reconciler reads. Uniqueness is therefore per-KID, not global.
        UniqueConstraint("kid", "authority", "value", name="uq_external_kid_authority_value"),
    )

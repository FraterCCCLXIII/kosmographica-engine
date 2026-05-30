"""FastAPI dependencies: read-only session + tier/sensitivity visibility policy."""

from __future__ import annotations

from collections.abc import Iterator

from fastapi import Query
from sqlalchemy.orm import Session

from ..config import settings
from ..db import SessionLocal
from ..models import Sensitivity, tiers_at_least

# Sensitivity levels the public read API will surface. sacred/restricted are gated
# (governance/ethics-and-sovereignty.md) and never returned by this unauthenticated API.
PUBLIC_SENSITIVITIES = [str(Sensitivity.PUBLIC), str(Sensitivity.SENSITIVE)]


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def visible_tiers(
    min_tier: str = Query(
        default=settings.public_min_tier,
        description="Lowest trust tier to include. The Audit Console passes "
        "`machine_unverified` to see everything; the public default hides it.",
    ),
) -> list[str]:
    return tiers_at_least(min_tier)

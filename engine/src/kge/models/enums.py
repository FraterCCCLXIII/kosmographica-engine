"""Controlled enumerations shared across the schema."""

from __future__ import annotations

from enum import StrEnum


class TrustTier(StrEnum):
    """Provenance trust tiers (ADR-012 / ADR-013).

    Ordered from least to most trusted. ``machine_unverified`` is hidden from the
    public API; everything at ``machine_validated`` and above is public-but-badged.
    """

    MACHINE_UNVERIFIED = "machine_unverified"
    MACHINE_VALIDATED = "machine_validated"
    HUMAN_REVIEWED = "human_reviewed"
    EXPERT_ENDORSED = "expert_endorsed"


# Tier ordering for "at least this tier" comparisons.
TIER_RANK: dict[str, int] = {
    TrustTier.MACHINE_UNVERIFIED: 0,
    TrustTier.MACHINE_VALIDATED: 1,
    TrustTier.HUMAN_REVIEWED: 2,
    TrustTier.EXPERT_ENDORSED: 3,
}


def tier_at_least(tier: str, minimum: str) -> bool:
    """True if ``tier`` is at least as trusted as ``minimum``."""
    return TIER_RANK.get(tier, -1) >= TIER_RANK.get(minimum, 99)


class Sensitivity(StrEnum):
    """Data-sovereignty sensitivity (governance/ethics-and-sovereignty.md)."""

    PUBLIC = "public"
    SENSITIVE = "sensitive"
    SACRED = "sacred"
    RESTRICTED = "restricted"


class AboutKind(StrEnum):
    """What a claim is about."""

    ENTITY = "entity"
    RELATIONSHIP = "relationship"

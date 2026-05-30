"""Canonical identifier (KID) minting.

Per `docs/architecture/identifiers-and-versioning.md`: KIDs are opaque, time-ordered
UUIDv7 values namespaced by record kind, e.g. ``kg:entity/018f...``. They carry no
semantics and never change once minted.
"""

from __future__ import annotations

import secrets
import time
import uuid

# Record-kind namespaces used in the KID prefix.
ENTITY = "entity"
RELATIONSHIP = "relationship"
CLAIM = "claim"
SOURCE = "source"


def uuid7() -> uuid.UUID:
    """Generate a UUIDv7 (RFC 9562): 48-bit ms timestamp + random, time-ordered."""
    ms = int(time.time() * 1000) & ((1 << 48) - 1)
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (ms << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    return uuid.UUID(int=value)


def kid(kind: str) -> str:
    """Mint a fresh KID for the given record kind."""
    return f"kg:{kind}/{uuid7()}"


# Zero-arg helpers for use as SQLAlchemy column defaults.
def entity_kid() -> str:
    return kid(ENTITY)


def relationship_kid() -> str:
    return kid(RELATIONSHIP)


def claim_kid() -> str:
    return kid(CLAIM)


def source_kid() -> str:
    return kid(SOURCE)

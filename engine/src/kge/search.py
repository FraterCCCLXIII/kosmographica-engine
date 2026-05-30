"""Shared full-text search expression (Postgres FTS, ADR-006).

The same ``to_tsvector`` expression backs the GIN index (migration 0002) and the query
in the read API, so plan and index stay aligned.
"""

from __future__ import annotations

from sqlalchemy import func

from .models import Entity


# Document side of the FTS match — must mirror migration 0002's index expression.
def entity_document():
    return func.to_tsvector(
        "simple",
        func.concat(
            func.coalesce(Entity.label, ""),
            " ",
            func.coalesce(Entity.data["description"].astext, ""),
        ),
    )


def fts_match(query: str):
    """A boolean SQL expression: does the entity document match ``query``?"""
    return entity_document().op("@@")(func.plainto_tsquery("simple", query))


def fts_rank(query: str):
    return func.ts_rank(entity_document(), func.plainto_tsquery("simple", query))

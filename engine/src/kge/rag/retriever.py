"""Retrieval implementations.

The corpus in Wave 2 is the canonical store itself: an entity's sourced
description is grounding text an author can summarise or relate. ``KeywordRetriever``
finds entities by full-text search, then expands one hop along relationships so the
author sees adjacent context. Each retrieved entity becomes a :class:`SourceDoc`
whose ``text`` is the material the author must quote verbatim.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..authoring import SourceDoc
from ..models import Entity, Relationship
from ..search import fts_match, fts_rank


@runtime_checkable
class Retriever(Protocol):
    name: str

    def retrieve(self, query: str, k: int = 5) -> list[SourceDoc]: ...


def _entity_text(entity: Entity) -> str:
    desc = (entity.data or {}).get("description")
    return desc.strip() if isinstance(desc, str) and desc.strip() else entity.label


def _doc_for(entity: Entity) -> SourceDoc:
    return SourceDoc(
        ref=f"ent_{entity.id.split('/')[-1]}",
        citation=f"Kosmographica entity: {entity.label} ({entity.id})",
        text=_entity_text(entity),
        uri=None,
    )


class KeywordRetriever:
    """FTS over entities + optional 1-hop neighbour expansion."""

    name = "keyword-retriever"

    def __init__(self, session: Session, *, expand_hops: int = 1) -> None:
        self.session = session
        self.expand_hops = expand_hops

    def retrieve(self, query: str, k: int = 5) -> list[SourceDoc]:
        if not query.strip():
            return []
        rows = self.session.execute(
            select(Entity)
            .where(fts_match(query))
            .order_by(fts_rank(query).desc())
            .limit(k)
        ).scalars().all()

        docs: dict[str, SourceDoc] = {}
        for entity in rows:
            docs.setdefault(entity.id, _doc_for(entity))
            if self.expand_hops:
                for neighbour in self._neighbours(entity.id):
                    docs.setdefault(neighbour.id, _doc_for(neighbour))
        return list(docs.values())

    def _neighbours(self, kid: str) -> list[Entity]:
        related_ids = self.session.execute(
            select(Relationship.object_id).where(Relationship.subject_id == kid)
            .union(select(Relationship.subject_id).where(Relationship.object_id == kid))
        ).scalars().all()
        if not related_ids:
            return []
        return self.session.execute(
            select(Entity).where(Entity.id.in_(related_ids))
        ).scalars().all()

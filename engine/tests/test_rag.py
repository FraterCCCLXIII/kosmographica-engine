"""W2.1: keyword retriever (FTS + 1-hop graph expansion). DB-backed."""

from __future__ import annotations

from kge.envelope import EntityIn, Envelope, RelationshipIn
from kge.pipeline import ingest
from kge.rag import KeywordRetriever, Retriever


def _seed(session):
    env = Envelope(
        source_system="test",
        generator="t",
        requires_grounding=False,
        entities=[
            EntityIn(
                ref="zeus",
                module="religion-mythology",
                type="Deity",
                label="Zeus",
                external_id="zeus",
                data={"description": "Zeus is the king of the Greek gods and ruler of Olympus."},
            ),
            EntityIn(
                ref="hera",
                module="religion-mythology",
                type="Deity",
                label="Hera",
                external_id="hera",
                data={"description": "Hera is the queen of the Greek gods, wife of Zeus."},
            ),
        ],
        relationships=[
            RelationshipIn(ref="r1", subject="zeus", predicate="spouseOf", object="hera", external_id="r1"),
        ],
    )
    return ingest(session, env)


def test_keyword_retriever_finds_and_expands(db_session):
    _seed(db_session)
    db_session.flush()
    retriever = KeywordRetriever(db_session, expand_hops=1)
    assert isinstance(retriever, Retriever)

    docs = retriever.retrieve("king of the gods", k=5)
    texts = " ".join(d.text for d in docs)
    assert "Zeus" in texts
    # 1-hop expansion pulls in the spouse (Hera) even though she didn't match the query.
    assert any("Hera" in d.text for d in docs)


def test_keyword_retriever_empty_query(db_session):
    _seed(db_session)
    assert KeywordRetriever(db_session).retrieve("   ") == []

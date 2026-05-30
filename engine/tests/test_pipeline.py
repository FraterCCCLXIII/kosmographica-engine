from sqlalchemy import func, select

from kge.adapters import mythographica_to_envelope
from kge.models import Claim, Entity, Relationship
from kge.pipeline import ingest
from kge.search import fts_match


def _graph() -> dict:
    return {
        "meta": {"title": "T", "version": "0.1"},
        "nodes": [
            {
                "id": "greek_zeus",
                "name": "Zeus",
                "type": "deity",
                "tradition": "Greek",
                "description": "Sky-father and king of the Olympian gods.",
                "confidenceLevel": "high",
                "sources": ["West 2007"],
                "attestedFrom": -800,
            },
            {
                "id": "pie_dyeus",
                "name": "*Dyeus",
                "type": "reconstructed_deity",
                "description": "Reconstructed Indo-European daylight-sky father.",
                "confidenceLevel": "medium",
                "sources": ["Mallory & Adams"],
            },
        ],
        "edges": [
            {
                "id": "e_dyeus_zeus",
                "source": "pie_dyeus",
                "target": "greek_zeus",
                "relationType": "linguistic_cognate",
                "confidence": 0.98,
                "explanation": "Zeus is a Greek reflex of the IE sky-god name.",
                "sources": ["West 2007"],
            }
        ],
    }


def test_ingest_loads_entities_relationships_claims(db_session):
    env = mythographica_to_envelope(_graph(), batch_id="t1")
    result = ingest(db_session, env)
    assert result.ok, result.report.errors
    assert result.counts["entities_created"] == 2
    assert result.counts["relationships_created"] == 1
    assert result.counts["claims_created"] == 3  # 2 node + 1 edge

    zeus = db_session.scalar(select(Entity).where(Entity.external_id == "greek_zeus"))
    assert zeus.tier == "machine_validated"  # curated source import
    assert zeus.valid_from == -800

    rel = db_session.scalar(select(Relationship))
    assert rel.subject_id == db_session.scalar(
        select(Entity.id).where(Entity.external_id == "pie_dyeus")
    )


def test_ingest_is_idempotent(db_session):
    env = mythographica_to_envelope(_graph(), batch_id="t1")
    ingest(db_session, env)
    db_session.flush()
    second = ingest(db_session, mythographica_to_envelope(_graph(), batch_id="t2"))
    assert second.counts["entities_created"] == 0
    assert second.counts["entities_matched"] == 2
    assert second.counts["claims_skipped"] >= 3
    assert second.counts["claims_created"] == 0


def test_fts_index_finds_entity(db_session):
    ingest(db_session, mythographica_to_envelope(_graph()))
    db_session.flush()
    hit = db_session.scalar(select(Entity.label).where(fts_match("olympian king")))
    assert hit == "Zeus"


def test_quarantine_on_validation_failure(db_session):
    env = mythographica_to_envelope(_graph())
    env.relationships[0].object = "ghost_node"  # unresolved
    result = ingest(db_session, env)
    assert result.quarantined
    assert not result.ok
    assert db_session.scalar(select(func.count()).select_from(Entity)) == 0

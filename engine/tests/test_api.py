import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from kge.adapters import mythographica_to_envelope
from kge.api.app import app
from kge.api.deps import get_session
from kge.models import Entity, TrustTier
from kge.pipeline import ingest


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
            },
            {
                "id": "greek_hera",
                "name": "Hera",
                "type": "deity",
                "tradition": "Greek",
                "description": "Queen of the gods, goddess of marriage.",
                "confidenceLevel": "high",
                "sources": ["West 2007"],
            },
        ],
        "edges": [
            {
                "id": "e_zeus_hera",
                "source": "greek_zeus",
                "target": "greek_hera",
                "relationType": "consort",
                "confidence": 0.9,
                "explanation": "Zeus and Hera are consorts in Greek myth.",
                "sources": ["West 2007"],
            }
        ],
    }


@pytest.fixture
def client(db_session):
    ingest(db_session, mythographica_to_envelope(_graph(), batch_id="b1"))
    # An AI-authored, not-yet-verified entity that must stay hidden by default.
    db_session.add(
        Entity(
            module="religion-mythology",
            type="Deity",
            label="Hidden Draft Deity",
            source_system="ai",
            external_id="draft_1",
            tier=TrustTier.MACHINE_UNVERIFIED,
            generator="gpt-test",
        )
    )
    db_session.flush()
    app.dependency_overrides[get_session] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


def _zeus_kid(db_session) -> str:
    return db_session.scalar(select(Entity.id).where(Entity.external_id == "greek_zeus"))


def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_list_entities_hides_unverified_by_default(client):
    body = client.get("/v1/entities", params={"module": "religion-mythology"}).json()
    labels = {i["label"] for i in body["items"]}
    assert {"Zeus", "Hera"} <= labels
    assert "Hidden Draft Deity" not in labels  # machine_unverified hidden


def test_list_entities_shows_unverified_for_audit(client):
    body = client.get(
        "/v1/entities", params={"module": "religion-mythology", "min_tier": "machine_unverified"}
    ).json()
    assert "Hidden Draft Deity" in {i["label"] for i in body["items"]}


def test_entity_detail_includes_claims(client, db_session):
    resp = client.get(f"/v1/entities/{_zeus_kid(db_session)}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["label"] == "Zeus"
    assert any("king of the Olympian" in c["assertion"] for c in body["claims"])
    assert body["claims"][0]["sources"][0]["citation"] == "West 2007"


def test_search(client):
    hits = client.get("/v1/search", params={"q": "marriage goddess"}).json()
    assert hits and hits[0]["entity"]["label"] == "Hera"


def test_graph_neighborhood(client, db_session):
    body = client.get(f"/v1/entities/{_zeus_kid(db_session)}/graph").json()
    assert len(body["nodes"]) == 2
    assert len(body["edges"]) == 1
    assert body["edges"][0]["predicate"] == "consort"


def test_audit_claim_detail_shows_verifications(client, db_session):
    from kge.authoring import SentenceAuthor, SourceDoc, author_envelope
    from kge.verify import publish_then_verify

    zeus = _zeus_kid(db_session)
    source = SourceDoc(ref="d", citation="Burkert", text="Zeus is the king of the gods.")
    publish_then_verify(db_session, author_envelope(SentenceAuthor(min_len=5), source, about=zeus, batch_id="aiX"))
    db_session.flush()

    queue = client.get("/v1/audit/claims", params={"batch_id": "aiX"}).json()
    assert queue["total"] >= 1
    claim_id = queue["items"][0]["id"]
    detail = client.get(f"/v1/audit/claims/{claim_id}").json()
    assert detail["verifications"]
    assert detail["verifications"][0]["support_label"] == "entailed"


def test_audit_stats_and_queue(client):
    stats = client.get("/v1/audit/stats").json()
    assert stats["claims_by_tier"].get("machine_validated", 0) >= 3

    queue = client.get("/v1/audit/claims", params={"tier": "machine_validated"}).json()
    assert queue["total"] >= 3
    assert all(i["tier"] == "machine_validated" for i in queue["items"])
    assert any(i["about_label"] == "Zeus" for i in queue["items"])

"""W2.2: cross-source entity resolution — proposals, sameAs, no name-only auto-merge."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import select

from kge.api.app import app
from kge.api.deps import get_session
from kge.envelope import EntityIn, Envelope, ExternalIdIn
from kge.models import Reconciliation, Relationship
from kge.pipeline import ingest
from kge.reconcile import accept, propose_matches, reconciliation_stats, reject, source_parity
from kge.reconcile.engine import SAMEAS_PREDICATE


def _entity(ref, label, *, external_ids=None):
    return EntityIn(
        ref=ref, external_id=ref, module="religion-mythology", type="Concept",
        label=label, data={"description": f"{label} description."},
        external_ids=external_ids or [],
    )


def _ingest_source(session, source_system, entities):
    ingest(session, Envelope(source_system=source_system, generator="t", entities=entities))
    session.flush()


def test_name_match_is_proposed_not_auto_linked(db_session):
    _ingest_source(db_session, "mythographica", [_entity("brahman_m", "Brahman")])
    _ingest_source(db_session, "sacred_lineage", [_entity("brahman_s", "Brahman")])

    summary = propose_matches(db_session)
    assert summary.proposed == 1
    assert summary.deterministic == 0

    row = db_session.scalar(select(Reconciliation))
    assert row.match_method == "scored"
    assert row.status == "proposed"  # name alone never auto-merges
    assert row.left_source != row.right_source
    # No sameAs relationship until a human accepts.
    assert db_session.scalar(select(Relationship).where(Relationship.predicate == SAMEAS_PREDICATE)) is None


def test_shared_external_id_auto_accepts(db_session):
    xid = [ExternalIdIn(authority="wikidata", value="Q9184")]
    _ingest_source(db_session, "mythographica", [_entity("logos_m", "Logos", external_ids=xid)])
    _ingest_source(db_session, "sacred_lineage", [_entity("logos_s", "Logos (concept)", external_ids=xid)])

    summary = propose_matches(db_session)
    assert summary.deterministic == 1
    row = db_session.scalar(select(Reconciliation).where(Reconciliation.match_method == "deterministic"))
    assert row.status == "accepted"
    # Auto-accept writes the non-destructive sameAs edge.
    rel = db_session.scalar(select(Relationship).where(Relationship.predicate == SAMEAS_PREDICATE))
    assert rel is not None and rel.source_system == "reconciliation"


def test_accept_creates_sameas_and_reject_is_remembered(db_session):
    _ingest_source(db_session, "mythographica", [_entity("a_m", "Nonduality")])
    _ingest_source(db_session, "sacred_lineage", [_entity("a_s", "Nonduality")])
    propose_matches(db_session)
    row = db_session.scalar(select(Reconciliation))

    assert accept(db_session, row.id) is True
    assert db_session.scalar(select(Relationship).where(Relationship.predicate == SAMEAS_PREDICATE)) is not None

    # Re-running does not duplicate an already-decided pair.
    summary2 = propose_matches(db_session)
    assert summary2.proposed == 0

    # Reject a fresh pair and confirm it is not re-proposed.
    _ingest_source(db_session, "mythographica", [_entity("b_m", "Emptiness")])
    _ingest_source(db_session, "sacred_lineage", [_entity("b_s", "Emptiness")])
    propose_matches(db_session)
    pending = db_session.scalar(
        select(Reconciliation).where(Reconciliation.status == "proposed")
    )
    assert reject(db_session, pending.id, "different traditions") is True
    before = len(db_session.scalars(select(Reconciliation)).all())
    propose_matches(db_session)
    after = len(db_session.scalars(select(Reconciliation)).all())
    assert before == after  # rejected pair remembered


def test_no_match_across_different_types(db_session):
    # Same label, different type => not blocked together.
    _ingest_source(db_session, "mythographica", [
        EntityIn(ref="x", external_id="x", module="religion-mythology", type="Deity", label="Shared"),
    ])
    _ingest_source(db_session, "sacred_lineage", [
        EntityIn(ref="y", external_id="y", module="religion-mythology", type="Figure", label="Shared"),
    ])
    summary = propose_matches(db_session)
    assert summary.proposed == 0


def test_reconciliation_stats(db_session):
    _ingest_source(db_session, "mythographica", [_entity("s_m", "Tawhid")])
    _ingest_source(db_session, "sacred_lineage", [_entity("s_s", "Tawhid")])
    propose_matches(db_session)
    stats = reconciliation_stats(db_session)
    assert stats["total"] == 1
    assert stats["by_status"].get("proposed") == 1


def test_parity_tolerates_partial_but_requires_keys(db_session):
    _ingest_source(db_session, "sacred_lineage", [_entity("p1", "Rigpa")])
    parity = source_parity(db_session, "sacred_lineage")
    assert parity["entities"] == 1
    assert parity["entities_missing_external_id"] == 0
    assert parity["converged"] is True


def test_reconcile_api_proposals_and_parity(db_session):
    _ingest_source(db_session, "mythographica", [_entity("api_m", "Logos")])
    _ingest_source(db_session, "sacred_lineage", [_entity("api_s", "Logos")])
    propose_matches(db_session)
    db_session.flush()

    app.dependency_overrides[get_session] = lambda: db_session
    try:
        client = TestClient(app)
        proposals = client.get("/v1/reconcile/proposals", params={"status": "proposed"}).json()
        assert proposals["total"] == 1
        item = proposals["items"][0]
        assert item["match_method"] == "scored"
        assert item["left"]["label"] == "Logos" and item["right"]["label"] == "Logos"
        assert item["left"]["source_system"] != item["right"]["source_system"]

        stats = client.get("/v1/reconcile/stats").json()
        assert stats["total"] == 1

        parity = client.get("/v1/reconcile/parity").json()
        assert {p["source_system"] for p in parity} == {"mythographica", "sacred_lineage"}
    finally:
        app.dependency_overrides.clear()

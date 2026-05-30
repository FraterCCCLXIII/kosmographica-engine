from sqlalchemy import func, select

from kge.adapters import mythographica_to_envelope
from kge.authoring import (
    ProposedClaim,
    SentenceAuthor,
    SourceDoc,
    author_envelope,
    build_grounded_envelope,
)
from kge.models import Claim, Entity, TrustTier, Verification
from kge.pipeline import ingest
from kge.verify import (
    lexical_entailment,
    publish_then_verify,
    reverify,
    spans_present,
)

# --- unit: verifier primitives (no DB) ---

def test_spans_present_detects_fabrication():
    src = "Zeus is the king of the gods."
    assert spans_present(["Zeus is the king of the gods"], src)
    assert not spans_present(["Zeus invented the telephone"], src)


def test_lexical_entailment_scores():
    assert lexical_entailment("Zeus is king of the gods", ["Zeus is the king of the gods"]) == 1.0
    assert lexical_entailment("Poseidon rules the deep sea", ["Zeus is king of the gods"]) < 0.3


def test_sentence_author_grounds_every_claim():
    src = SourceDoc(ref="s", citation="Test", text="Zeus is the king of the gods. He wields thunder.")
    proposals = SentenceAuthor(min_len=10).propose(src, about="kg:entity/x")
    assert proposals
    assert all(p.quotes and p.quotes[0] in src.text for p in proposals)


# --- DB-backed: the publish-then-verify loop ---

def _seed_zeus(db_session) -> str:
    graph = {
        "meta": {},
        "nodes": [
            {
                "id": "greek_zeus",
                "name": "Zeus",
                "type": "deity",
                "description": "King of the Olympian gods.",
                "sources": ["West 2007"],
            }
        ],
        "edges": [],
    }
    ingest(db_session, mythographica_to_envelope(graph))
    db_session.flush()
    return db_session.scalar(select(Entity.id).where(Entity.external_id == "greek_zeus"))


def test_grounded_claims_are_accepted_and_promoted(db_session):
    zeus = _seed_zeus(db_session)
    source = SourceDoc(
        ref="src_doc",
        citation="Burkert, Greek Religion",
        text="Zeus is the king of the gods. Zeus wields the thunderbolt as his weapon.",
    )
    env = author_envelope(SentenceAuthor(min_len=10), source, about=zeus, batch_id="ai1")
    result = publish_then_verify(db_session, env)

    assert not result.quarantined
    assert result.accepted == 2 and result.rejected == 0
    promoted = db_session.scalars(
        select(Claim).where(Claim.batch_id == "ai1", Claim.tier == TrustTier.MACHINE_VALIDATED)
    ).all()
    assert len(promoted) == 2
    assert all(c.confidence >= 0.6 for c in promoted)
    # Every routed claim has a recorded verification (auditability).
    assert db_session.scalar(select(func.count()).select_from(Verification)) == 2


def test_fabricated_span_is_rejected_and_hidden(db_session):
    zeus = _seed_zeus(db_session)
    source = SourceDoc(ref="src_doc", citation="Some source", text="Zeus is the king of the gods.")
    env = build_grounded_envelope(
        source,
        about=zeus,
        proposals=[ProposedClaim(assertion="Zeus founded Athens", quotes=["Zeus founded Athens in 600 BCE"])],
        generator="gpt-test",
        batch_id="ai2",
    )
    result = publish_then_verify(db_session, env)
    assert result.rejected == 1 and result.accepted == 0
    claim = db_session.scalar(select(Claim).where(Claim.batch_id == "ai2"))
    assert claim.tier == TrustTier.MACHINE_UNVERIFIED  # hidden from public
    verification = db_session.scalar(select(Verification).where(Verification.claim_id == claim.id))
    assert verification.support_label == "fabricated"


def test_unsupported_claim_is_rejected(db_session):
    zeus = _seed_zeus(db_session)
    source = SourceDoc(ref="src_doc", citation="Src", text="Zeus is the king of the gods.")
    env = build_grounded_envelope(
        source,
        about=zeus,
        # span is real, but the assertion is not entailed by it
        proposals=[ProposedClaim(
            assertion="Poseidon commands earthquakes beneath the ocean floor",
            quotes=["Zeus is the king of the gods"],
        )],
        generator="gpt-test",
        batch_id="ai3",
    )
    result = publish_then_verify(db_session, env)
    assert result.rejected == 1
    verification = db_session.scalar(select(Verification))
    assert verification.support_label == "not_entailed"


def test_reverify_recomputes(db_session):
    zeus = _seed_zeus(db_session)
    source = SourceDoc(ref="src_doc", citation="Src", text="Zeus is the king of the gods.")
    env = author_envelope(SentenceAuthor(min_len=5), source, about=zeus, batch_id="ai4")
    publish_then_verify(db_session, env)
    summary = reverify(db_session, batch_id="ai4")
    assert summary["checked"] >= 1
    assert summary["accept"] >= 1

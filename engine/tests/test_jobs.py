"""W2.3: continuous re-verification job emits an audit delta."""

from __future__ import annotations

from sqlalchemy import func, select

from kge.authoring import LLMAuthor, SourceDoc, author_envelope
from kge.jobs import run_reverify
from kge.llm import FakeLLMClient
from kge.models import Claim, Verification
from kge.verify import Verifier, make_llm_verifier, publish_then_verify


def _seed_grounded(session, *, batch_id="b1"):
    src = SourceDoc(ref="s1", citation="Test", text="Zeus is the king of the gods and rules the sky.")
    env = author_envelope(LLMAuthor(FakeLLMClient()), src, about="kg:entity/zeus", batch_id=batch_id)
    # Ensure the about entity exists so claims attach (about is a literal kid here).
    return publish_then_verify(session, env, verifier=make_llm_verifier(FakeLLMClient()))


def test_reverify_job_reports_delta(db_session):
    result = _seed_grounded(db_session)
    assert result.accepted >= 1
    db_session.flush()

    delta = run_reverify(db_session, batch_id=result.batch_id, verifier=make_llm_verifier(FakeLLMClient()))
    d = delta.as_dict()
    assert d["checked"] >= 1
    assert d["outcomes"]["accept"] >= 1
    # A fresh verification row is recorded for every re-checked claim (audit trail).
    verifs = db_session.scalar(select(func.count()).select_from(Verification))
    assert verifs >= d["checked"]


def test_reverify_threshold_change_decays_tier(db_session):
    _seed_grounded(db_session, batch_id="b2")
    db_session.flush()
    accepted_before = db_session.scalar(
        select(func.count()).select_from(Claim).where(
            Claim.batch_id == "b2", Claim.tier == "machine_validated"
        )
    )
    assert accepted_before >= 1

    # An impossibly strict verifier should demote previously-accepted claims.
    strict = Verifier(accept_threshold=1.01)
    delta = run_reverify(db_session, batch_id="b2", verifier=strict)
    assert delta.reject >= 1
    assert delta.as_dict()["tier_delta"].get("machine_unverified", 0) >= 1

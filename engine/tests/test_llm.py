"""W2.1: provider-agnostic LLM client, LLM author, and the verifier eval gate."""

from __future__ import annotations

import json

from kge.authoring import LLMAuthor, SourceDoc, author_envelope
from kge.eval import evaluate, load_gold, run_eval
from kge.llm import FakeLLMClient, get_llm_client
from kge.llm._entail_prompt import parse_score
from kge.verify import Verifier, make_llm_verifier


def test_factory_defaults_to_fake():
    client = get_llm_client()
    assert isinstance(client, FakeLLMClient)
    assert client.name == "fake-llm"


def test_fake_entail_is_lexical_and_bounded():
    client = FakeLLMClient()
    assert client.entail("Zeus is king of the gods", "Zeus is king of the gods") == 1.0
    assert 0.0 <= client.entail("the sky is blue", "Poseidon rules the sea") < 0.3


def test_parse_score_robust():
    assert parse_score("0.8") == 0.8
    assert parse_score("Score: 1.0 (fully supported)") == 1.0
    assert parse_score("nonsense") == 0.0
    assert parse_score("1.5") == 1.0  # clamped to [0,1]


def test_llm_author_extracts_grounded_claims_offline():
    src = SourceDoc(
        ref="s1",
        citation="Test source",
        text="Zeus is the king of the gods. He rules Mount Olympus and the sky.",
    )
    author = LLMAuthor(FakeLLMClient())
    proposals = author.propose(src, about="kg:entity/zeus")
    assert proposals
    for p in proposals:
        assert p.quotes
        assert all(q in src.text for q in p.quotes)


def test_llm_author_drops_fabricated_quotes():
    # Scripted client returns a claim whose quote is NOT in the source.
    fabricated = json.dumps([{"assertion": "Zeus invented the telephone", "quotes": ["Zeus invented the telephone"]}])
    src = SourceDoc(ref="s1", citation="Test", text="Zeus is the king of the gods.")
    author = LLMAuthor(FakeLLMClient(responses=[fabricated]))
    assert author.propose(src, about="kg:entity/zeus") == []


def test_author_envelope_is_grounded():
    src = SourceDoc(ref="s1", citation="Test", text="Athena is the goddess of wisdom and warfare.")
    env = author_envelope(LLMAuthor(FakeLLMClient()), src, about="kg:entity/athena")
    assert env.requires_grounding is True
    assert env.generator.startswith("llm-author:")
    assert env.claims and all(c.support_spans for c in env.claims)


def test_make_llm_verifier_uses_client_signal():
    verifier = make_llm_verifier(FakeLLMClient(), accept_threshold=0.6)
    assert verifier.name == "nli-verifier:fake-llm"
    ok = verifier.verify(
        assertion="Zeus is king of the gods",
        quotes=["Zeus is the king of the gods in Greek religion"],
        source_text="Zeus is the king of the gods in Greek religion.",
    )
    assert ok.outcome == "accept"


def test_eval_gate_fake_matches_baseline():
    gold = load_gold()
    assert len(gold) >= 10
    baseline = evaluate(Verifier(), gold)
    assert baseline.n == len(gold)
    report = run_eval(FakeLLMClient())
    # Fake entailment == lexical baseline, so the gate passes (no regression).
    assert report.passed
    assert report.candidate.f1 >= report.baseline.f1

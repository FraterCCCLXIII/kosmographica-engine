from kge.envelope import (
    ClaimIn,
    Envelope,
    EntityIn,
    RelationshipIn,
    SourceIn,
    SupportSpan,
)
from kge.validation import validate_envelope


def _good_envelope() -> Envelope:
    return Envelope(
        source_system="mythographica",
        generator="test",
        sources=[SourceIn(ref="s1", citation="Hesiod, Theogony", uri="urn:cts:greekLit:tlg0020.tlg001")],
        entities=[
            EntityIn(ref="zeus", module="religion-mythology", type="Deity", label="Zeus"),
            EntityIn(ref="hera", module="religion-mythology", type="Deity", label="Hera"),
        ],
        relationships=[
            RelationshipIn(ref="r1", subject="zeus", predicate="spouse_of", object="hera")
        ],
        claims=[
            ClaimIn(
                about="zeus",
                assertion="Zeus is king of the gods.",
                source_refs=["s1"],
                support_spans=[SupportSpan(source_ref="s1", quote="Zeus who is lord of all")],
            )
        ],
    )


def test_good_envelope_passes():
    report = validate_envelope(_good_envelope())
    assert report.ok, report.errors


def test_unresolved_relationship_target_quarantines():
    env = _good_envelope()
    env.relationships[0].object = "poseidon"  # not defined
    report = validate_envelope(env)
    assert not report.ok
    assert any(i.code == "rel.unresolved_object" for i in report.errors)


def test_claim_without_source_or_span_fails():
    env = _good_envelope()
    env.claims[0].source_refs = []
    env.claims[0].support_spans = []
    report = validate_envelope(env)
    codes = {i.code for i in report.errors}
    assert {"claim.no_source", "claim.no_support_span"} <= codes


def test_confidence_out_of_range_fails():
    env = _good_envelope()
    env.claims[0].confidence = 1.7
    report = validate_envelope(env)
    assert any(i.code == "claim.confidence_range" for i in report.errors)


def test_unknown_source_ref_in_claim_fails():
    env = _good_envelope()
    env.claims[0].source_refs = ["ghost"]
    report = validate_envelope(env)
    assert any(i.code == "claim.unknown_source_ref" for i in report.errors)

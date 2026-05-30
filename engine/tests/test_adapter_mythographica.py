import json
from pathlib import Path

import pytest

from kge.adapters import mythographica_to_envelope
from kge.validation import validate_envelope

STARTER = Path(
    "/Users/paulbloch/Documents/github/Interpretatio-Universalis/eurasian-deity-graph-starter.json"
)


def _mini_graph() -> dict:
    return {
        "meta": {"title": "Test", "version": "0.0.1"},
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
                "name": "*Dyēus",
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
                "label": "name cognate",
                "confidence": 0.98,
                "directed": True,
                "explanation": "Zeus is a Greek reflex of the IE sky-god name.",
                "sources": ["West 2007"],
            }
        ],
    }


def test_adapter_maps_nodes_edges_and_dedupes_sources():
    env = mythographica_to_envelope(_mini_graph())
    assert env.source_system == "mythographica"
    assert env.requires_grounding is False
    assert {e.ref for e in env.entities} == {"greek_zeus", "pie_dyeus"}

    zeus = next(e for e in env.entities if e.ref == "greek_zeus")
    assert zeus.type == "Deity" and zeus.subtype == "deity"
    assert zeus.valid_from == -800
    assert zeus.data["tradition"] == "Greek"

    # "West 2007" appears on a node and an edge -> one shared source.
    assert sum(1 for s in env.sources if s.citation == "West 2007") == 1

    rel = env.relationships[0]
    assert rel.predicate == "linguistic_cognate"
    rel_claim = next(c for c in env.claims if c.about_kind == "relationship")
    assert rel_claim.confidence == pytest.approx(0.98)


def test_adapter_output_validates():
    report = validate_envelope(mythographica_to_envelope(_mini_graph()))
    assert report.ok, report.errors


@pytest.mark.skipif(not STARTER.exists(), reason="starter dataset not present")
def test_real_starter_converts_and_validates():
    graph = json.loads(STARTER.read_text())
    env = mythographica_to_envelope(graph, batch_id="starter")
    assert len(env.entities) == len(graph["nodes"])
    report = validate_envelope(env)
    assert report.ok, report.errors[:5]

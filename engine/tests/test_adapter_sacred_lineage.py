"""W2.2: Sacred-Lineage adapter — mapping + partial-tolerance."""

from __future__ import annotations

from kge.adapters import sacred_lineage_to_envelope
from kge.adapters.sacred_lineage import SOURCE_SYSTEM


def _tables() -> dict:
    return {
        "traditions": [
            {"id": 1, "slug": "buddhism", "name": "Buddhism", "name_native": None,
             "description": "A tradition.", "region": "eastern", "year_founded": -500},
        ],
        "schools": [
            {"id": 5, "slug": "zen", "name": "Zen", "description": None, "year_founded": 600},
            {"id": 6, "slug": "noname", "name": None, "description": "orphan"},  # skipped: no name
        ],
        "lineage_charts": [{"id": 21, "slug": "ramana", "name": "Ramana lineage", "description": None}],
        "concepts": [
            {"id": 1, "slug": "sunyata", "name": "Sunyata", "name_native": None, "summary": "Emptiness."},
            {"id": 2, "slug": "brahman", "name": "Brahman", "summary": "Ultimate reality."},
        ],
        "texts": [{"id": 1, "slug": "heart", "title": "Heart Sutra", "summary": "A sutra.",
                   "approx_date_start": 100, "approx_date_end": 200, "text_kind": "sutra"}],
        "masters": [
            {"id": 1, "name": "Ramana Maharshi", "name_native": "ரமண", "overview": "An Indian sage.",
             "year_born": 1879, "year_died": 1950, "figure_kind": "historical", "gender": "male",
             "external_slug": None, "source_catalog": None, "source_url": None, "philosophy_tags": "advaita, nondual"},
            {"id": 20, "name": "Mahakashyapa", "overview": "A disciple.", "year_born": None, "year_died": None,
             "figure_kind": "historical", "external_slug": "rigpa-wiki/Mahakashyapa",
             "source_catalog": "rigpa-wiki", "source_url": "https://www.rigpawiki.org/x"},
            {"id": 99, "name": None, "overview": "no name"},  # skipped
        ],
        "relationship_types": [
            {"id": 1, "key": "guru_disciple", "name": "Guru-disciple", "domain": "person_person"},
            {"id": 30, "key": "compared_with", "name": "Compared with"},
        ],
        "relationships": [
            {"id": 1, "parent_master_id": 1, "child_master_id": 20, "relationship_type_id": 1, "lineage_id": 21},
            {"id": 2, "parent_master_id": 1, "child_master_id": 999, "relationship_type_id": 1, "lineage_id": None},  # dangling -> skipped
        ],
        "entity_links": [
            {"id": 1, "source_type": "concept", "source_id": 1, "target_type": "concept", "target_id": 2,
             "relationship_type_id": 30, "certainty": "disputed", "notes": "Debated mapping.", "citation": None},
        ],
    }


def test_adapter_maps_entities_relationships_claims():
    env = sacred_lineage_to_envelope(_tables())
    assert env.source_system == SOURCE_SYSTEM
    assert env.requires_grounding is False

    by_type: dict[str, int] = {}
    for e in env.entities:
        by_type[e.type] = by_type.get(e.type, 0) + 1
    assert by_type["Tradition"] == 1
    assert by_type["Concept"] == 2
    assert by_type["Figure"] == 2  # the no-name master is skipped
    assert by_type["Text"] == 1

    # External catalog id captured for cross-source matching.
    maha = next(e for e in env.entities if e.label == "Mahakashyapa")
    assert any(x.authority == "rigpa-wiki" for x in maha.external_ids)

    # Tags parsed into a list; valid-time from birth/death years.
    ramana = next(e for e in env.entities if e.label == "Ramana Maharshi")
    assert ramana.data["philosophy_tags"] == ["advaita", "nondual"]
    assert ramana.valid_from == 1879 and ramana.valid_to == 1950


def test_adapter_is_partial_tolerant():
    env = sacred_lineage_to_envelope(_tables())
    # 2 rows skipped (school id 6, master id 99) recorded, not fatal.
    assert env.meta["skipped_rows"] == 2

    # Dangling transmission (child 999 absent) dropped; valid one kept.
    transmissions = [r for r in env.relationships if r.ref.startswith("sl:transmission")]
    assert len(transmissions) == 1
    assert transmissions[0].predicate == "guru_disciple"

    # Concept<->concept comparison link kept with certainty metadata.
    link = next(r for r in env.relationships if r.ref.startswith("sl:entitylink"))
    assert link.predicate == "compared_with"
    assert link.data["certainty"] == "disputed"


def test_adapter_handles_empty_tables():
    env = sacred_lineage_to_envelope({})
    assert env.entities == [] and env.relationships == [] and env.claims == []
    assert env.source_system == SOURCE_SYSTEM

"""Tests for the controlled taxonomy classifier (kge.taxonomy)."""

from __future__ import annotations

from kge import taxonomy
from kge.taxonomy import apply_classification_data, classify


def test_plain_deity_is_mythic_and_clean():
    c = classify(myth_type="deity", label="Zeus")
    assert c.entity_type == taxonomy.DEITY
    assert c.subtype == "deity"
    assert c.status == taxonomy.STATUS_MYTHIC
    assert c.is_collective is False
    assert c.needs_review is False


def test_reconstructed_sets_status_not_type():
    c = classify(myth_type="reconstructed_deity", label="*Dyēus")
    assert c.entity_type == taxonomy.DEITY
    assert c.status == taxonomy.STATUS_RECONSTRUCTED


def test_historical_master_ontology_class_marks_historical():
    c = classify(myth_type="sage", ontology_class="historical_master", label="Tsongkhapa")
    assert c.entity_type == taxonomy.SAGE
    assert c.status == taxonomy.STATUS_HISTORICAL


def test_sage_without_signal_is_unknown_status():
    c = classify(myth_type="sage", label="Some Sage")
    assert c.entity_type == taxonomy.SAGE
    assert c.status == taxonomy.STATUS_UNKNOWN


def test_hero_and_mythic_king_are_legendary():
    assert classify(myth_type="hero", label="Heracles").status == taxonomy.STATUS_LEGENDARY
    assert classify(myth_type="mythic_king", label="Yu").status == taxonomy.STATUS_LEGENDARY


def test_previously_silent_deity_fallbacks_now_route_correctly():
    assert classify(myth_type="titan", label="Kronos").entity_type == taxonomy.PRIMORDIAL
    assert classify(myth_type="serpent_monster", label="Vritra").entity_type == taxonomy.DEMON
    assert classify(myth_type="chaos_serpent", label="Apep").entity_type == taxonomy.DEMON
    assert classify(myth_type="primordial_giant", label="Ymir").entity_type == taxonomy.PRIMORDIAL


def test_collectives_stay_deity_or_hero_with_subtype():
    for raw in ("deity_group", "deity_pair", "deity_class"):
        c = classify(myth_type=raw, label="The Twins")
        assert c.entity_type == taxonomy.DEITY, raw
        assert c.subtype == raw
        assert c.is_collective is True
        assert c.status == taxonomy.STATUS_MYTHIC
    c = classify(myth_type="hero_pair", label="The Twins")
    assert c.entity_type == taxonomy.HERO
    assert c.is_collective is True
    assert c.status == taxonomy.STATUS_LEGENDARY


def test_reconstructed_pair_stays_deity_collective():
    c = classify(myth_type="reconstructed_deity_pair", label="Divine Twins")
    assert c.entity_type == taxonomy.DEITY
    assert c.is_collective is True
    assert c.status == taxonomy.STATUS_RECONSTRUCTED
    assert c.needs_review is False


def test_numbered_and_plural_collective_names_stay_deity_and_flag():
    for label in ("Dragon Kings", "Five Suns", "Three Sisters", "Maya Hero Twins"):
        c = classify(myth_type="deity", label=label)
        assert c.entity_type == taxonomy.DEITY, label
        assert c.is_collective is True, label
        assert c.needs_review is True, label


def test_singular_divine_names_stay_deity():
    for label in ("Kitchen God", "Zeus Xenios", "Maya rain god", "Sol Invictus", "Dragon King"):
        c = classify(myth_type="deity", label=label)
        assert c.entity_type == taxonomy.DEITY, label
        assert c.is_collective is False, label


def test_ontology_class_group_refines_concept_to_deity():
    c = classify(myth_type="abstract_personification", ontology_class="group", label="Corybantes")
    assert c.entity_type == taxonomy.DEITY
    assert c.is_collective is True
    assert c.needs_review is True


def test_ontology_class_group_on_deity_stays_deity():
    c = classify(myth_type="deity", ontology_class="group", label="Saptarishi")
    assert c.entity_type == taxonomy.DEITY
    assert c.is_collective is True


def test_collective_name_heuristic_promotes_concept_to_deity():
    c = classify(myth_type="abstract_personification", label="The Adityas")
    assert c.entity_type == taxonomy.DEITY
    assert c.is_collective is True
    assert c.needs_review is True
    assert "collective" in (c.review_reason or "")


def test_plain_concept_is_not_a_collective():
    c = classify(myth_type="abstract_personification", label="Justice")
    assert c.entity_type == taxonomy.CONCEPT
    assert c.status is None
    assert c.is_collective is False
    assert c.needs_review is False


def test_unmapped_type_is_flagged_not_silently_deity():
    c = classify(myth_type="totally_new_kind", label="Mystery")
    assert c.entity_type == taxonomy.DEITY
    assert c.needs_review is True
    assert "unmapped" in (c.review_reason or "")


def test_ambiguous_type_keeps_guess_but_flags():
    c = classify(myth_type="reconstructed_myth", label="Theft of Fire")
    assert c.entity_type == taxonomy.MOTIF
    assert c.needs_review is True


def test_missing_type_is_flagged():
    c = classify(myth_type=None, label="Nameless")
    assert c.needs_review is True


def test_entity_class_not_in_canonical_types():
    assert "EntityClass" not in taxonomy.CANONICAL_ENTITY_TYPES


def test_apply_classification_data_sets_collective_flag():
    data = apply_classification_data({}, classify(myth_type="deity_group", label="Norns"))
    assert data["is_collective"] is True
    assert data["status"] == taxonomy.STATUS_MYTHIC


def test_all_mapped_types_yield_canonical_entity_types():
    for raw, expected in taxonomy.MYTH_TYPE_TO_ENTITY.items():
        c = classify(myth_type=raw, label="x")
        assert c.entity_type in taxonomy.CANONICAL_ENTITY_TYPES
        assert expected in taxonomy.CANONICAL_ENTITY_TYPES
        if c.status is not None:
            assert c.status in taxonomy.CANONICAL_STATUSES

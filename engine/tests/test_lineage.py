from datetime import UTC, datetime

from kge.lineage import build_lineage_out
from kge.models import Entity, Relationship, TrustTier


def _figure(kid: str, label: str, *, valid_from: int | None = None) -> Entity:
    return Entity(
        id=kid,
        module="religion-mythology",
        type="Figure",
        label=label,
        source_system="sacred_lineage",
        external_id=f"sl:figure:{label}",
        tier=TrustTier.MACHINE_VALIDATED,
        sensitivity="public",
        data={},
        recorded_at=datetime.now(UTC),
        valid_from=valid_from,
    )


def _chart() -> Entity:
    return Entity(
        id="kg:entity/chart1",
        module="religion-mythology",
        type="LineageChart",
        label="Test Lineage",
        source_system="sacred_lineage",
        external_id="sl:lineagechart:1",
        tier=TrustTier.MACHINE_VALIDATED,
        sensitivity="public",
        data={},
        recorded_at=datetime.now(UTC),
    )


def test_build_lineage_tree():
    chart = _chart()
    a, b, c = _figure("kg:a", "Root", valid_from=1000), _figure("kg:b", "Child"), _figure("kg:c", "Unlinked")
    rels = [
        Relationship(
            subject_id="kg:a",
            object_id="kg:b",
            predicate="transmitted_to",
            source_system="sacred_lineage",
            external_id="sl:transmission:1",
            tier=TrustTier.MACHINE_VALIDATED,
            data={"lineage_chart": "sl:lineagechart:1"},
        ),
        Relationship(
            subject_id="kg:x",
            object_id="kg:c",
            predicate="transmitted_to",
            source_system="sacred_lineage",
            external_id="sl:transmission:2",
            tier=TrustTier.MACHINE_VALIDATED,
            data={"lineage_chart": "sl:lineagechart:1"},
        ),
    ]
    out = build_lineage_out(chart, rels, [chart, a, b, c])
    assert out.transmission_count == 2
    assert len(out.roots) == 1
    assert out.roots[0].entity.id == "kg:a"
    assert len(out.roots[0].children) == 1
    assert out.roots[0].children[0].entity.id == "kg:b"
    assert out.roots[0].children[0].predicate == "transmitted_to"
    assert out.unlinked == []

"""Reclassify already-ingested entities against the controlled taxonomy.

The ingest pipeline is idempotent on ``(source_system, external_id)`` and never updates a
matched row (ADR-010), so adapter fixes only reach *future* data. This job recomputes
``type`` / ``subtype`` / ``data.status`` for entities already in the store, reading the
source signals that the adapter preserved in ``data`` (``myth_type``, ``ontologyClass``) —
no source re-read, no re-ingest.

Run with ``dry_run=True`` first: it reports the before/after type distribution and the
per-entity diffs without writing anything.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Entity
from ..taxonomy import apply_classification_data, classify

# Source system whose nodes carry the MythGraph ``myth_type`` / ``ontologyClass`` signals.
MYTHOGRAPHICA = "mythographica"


@dataclass
class EntityChange:
    kid: str
    label: str
    old_type: str
    new_type: str
    new_status: str | None
    needs_review: bool


@dataclass
class ReclassifyReport:
    scanned: int = 0
    changed: int = 0
    flagged_for_review: int = 0
    before_types: Counter = field(default_factory=Counter)
    after_types: Counter = field(default_factory=Counter)
    status_after: Counter = field(default_factory=Counter)
    changes: list[EntityChange] = field(default_factory=list)
    dry_run: bool = True

    def as_dict(self) -> dict:
        return {
            "dry_run": self.dry_run,
            "scanned": self.scanned,
            "changed": self.changed,
            "flagged_for_review": self.flagged_for_review,
            "before_types": dict(self.before_types.most_common()),
            "after_types": dict(self.after_types.most_common()),
            "status_after": dict(self.status_after.most_common()),
            "type_transitions": dict(
                Counter(
                    f"{c.old_type} -> {c.new_type}"
                    for c in self.changes
                    if c.old_type != c.new_type
                ).most_common()
            ),
        }


def reclassify_entities(
    session: Session,
    *,
    source_system: str = MYTHOGRAPHICA,
    dry_run: bool = True,
    limit: int | None = None,
) -> ReclassifyReport:
    report = ReclassifyReport(dry_run=dry_run)

    rows = session.scalars(
        select(Entity).where(Entity.source_system == source_system)
    ).all()

    for ent in rows:
        if limit is not None and report.scanned >= limit:
            break
        report.scanned += 1
        report.before_types[ent.type] += 1

        data = dict(ent.data or {})
        myth_type = data.get("myth_type")
        # Nodes without a source myth_type aren't from the MythGraph mapping; leave as-is.
        if myth_type is None:
            report.after_types[ent.type] += 1
            continue

        cls = classify(
            myth_type=myth_type,
            ontology_class=data.get("ontologyClass"),
            label=ent.label,
        )

        new_data = apply_classification_data(data, cls)

        type_changed = ent.type != cls.entity_type
        data_changed = new_data != data
        report.after_types[cls.entity_type] += 1
        if cls.status:
            report.status_after[cls.status] += 1
        if cls.needs_review:
            report.flagged_for_review += 1

        if type_changed or data_changed:
            report.changed += 1
            report.changes.append(
                EntityChange(
                    kid=ent.id,
                    label=ent.label,
                    old_type=ent.type,
                    new_type=cls.entity_type,
                    new_status=cls.status,
                    needs_review=cls.needs_review,
                )
            )
            if not dry_run:
                ent.type = cls.entity_type
                ent.subtype = cls.subtype
                ent.data = new_data  # reassign so SQLAlchemy flags the JSONB column dirty

    if not dry_run:
        session.flush()
    return report

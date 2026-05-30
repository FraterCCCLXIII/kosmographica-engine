"""Deterministic envelope validator — the single source of truth for "is this loadable?".

Per ADR-011, validation failures *quarantine* the offending records (the pipeline holds
them for inspection); they are never silently dropped. This module only classifies
issues; the pipeline decides what to do with a failing report.

Three check families:
  * structural  — shape, required fields, internal ref integrity
  * provenance  — every claim is sourced and grounded (support spans)
  * epistemic   — values are sane (confidence range, non-empty assertions/labels)
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..envelope import Envelope

SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
VALID_ABOUT_KINDS = {"entity", "relationship"}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    severity: str = "error"  # error -> quarantine; warning -> load with a flag
    where: str | None = None


@dataclass
class ValidationReport:
    issues: list[Issue] = field(default_factory=list)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, code: str, message: str, severity: str = "error", where: str | None = None) -> None:
        self.issues.append(Issue(code=code, message=message, severity=severity, where=where))


def validate_envelope(env: Envelope) -> ValidationReport:
    report = ValidationReport()
    _structural(env, report)
    _provenance(env, report)
    _epistemic(env, report)
    return report


def _structural(env: Envelope, report: ValidationReport) -> None:
    if env.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        report.add(
            "schema.unsupported",
            f"schema_version {env.schema_version!r} is not supported "
            f"(supported: {sorted(SUPPORTED_SCHEMA_VERSIONS)})",
        )
    if not env.source_system.strip():
        report.add("envelope.no_source_system", "source_system is required")

    entity_refs: set[str] = set()
    source_refs: set[str] = set()

    for e in env.entities:
        if e.ref in entity_refs:
            report.add("entity.duplicate_ref", f"duplicate entity ref {e.ref!r}", where=e.ref)
        entity_refs.add(e.ref)
        if not e.module.strip() or not e.type.strip():
            report.add("entity.missing_type", "entity needs module and type", where=e.ref)
        if not e.label.strip():
            report.add("entity.empty_label", "entity label is empty", where=e.ref)

    for s in env.sources:
        if s.ref in source_refs:
            report.add("source.duplicate_ref", f"duplicate source ref {s.ref!r}", where=s.ref)
        source_refs.add(s.ref)

    # KIDs already in the store are accepted as targets without resolving here.
    def resolves(ref: str) -> bool:
        return ref in entity_refs or ref.startswith("kg:")

    for r in env.relationships:
        if not resolves(r.subject):
            report.add("rel.unresolved_subject", f"subject {r.subject!r} not found", where=r.ref)
        if not resolves(r.object):
            report.add("rel.unresolved_object", f"object {r.object!r} not found", where=r.ref)
        if not r.predicate.strip():
            report.add("rel.empty_predicate", "relationship predicate is empty", where=r.ref)

    for i, c in enumerate(env.claims):
        loc = c.about
        if c.about_kind not in VALID_ABOUT_KINDS:
            report.add("claim.bad_about_kind", f"about_kind {c.about_kind!r} invalid", where=loc)
        if c.about_kind == "entity" and not resolves(c.about):
            report.add("claim.unresolved_about", f"claim about {c.about!r} not found", where=loc)
        for sref in c.source_refs:
            if sref not in source_refs:
                report.add(
                    "claim.unknown_source_ref",
                    f"claim cites unknown source ref {sref!r}",
                    where=loc,
                )
        for span in c.support_spans:
            if span.source_ref not in source_refs:
                report.add(
                    "span.unknown_source_ref",
                    f"support span cites unknown source ref {span.source_ref!r}",
                    where=loc,
                )


def _provenance(env: Envelope, report: ValidationReport) -> None:
    for c in env.claims:
        if not c.source_refs:
            report.add("claim.no_source", "claim has no source", where=c.about)
        # Grounded generation: a claim must point at the exact supporting text.
        if not c.support_spans:
            report.add(
                "claim.no_support_span",
                "claim has no support span (grounded generation required)",
                where=c.about,
            )
        else:
            for span in c.support_spans:
                if not span.quote.strip():
                    report.add("span.empty_quote", "support span quote is empty", where=c.about)


def _epistemic(env: Envelope, report: ValidationReport) -> None:
    for c in env.claims:
        if not c.assertion.strip():
            report.add("claim.empty_assertion", "claim assertion is empty", where=c.about)
        if c.confidence is not None and not (0.0 <= c.confidence <= 1.0):
            report.add(
                "claim.confidence_range",
                f"confidence {c.confidence} outside [0.0, 1.0]",
                where=c.about,
            )

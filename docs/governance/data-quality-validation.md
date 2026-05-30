# Data Quality & Validation

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the validation rules and quality gates that every record must pass before/within ingestion,
and the automated audits that monitor corpus health over time.

## Sections to detail

1. **Structural validation** — unique IDs, referential integrity (every relationship/claim endpoint
   exists), schema conformance, enum membership.
2. **Epistemic validation** — confidence ∈ [0,1]; speculative links require low confidence or stated
   methodology; never equate linguistic cognate / functional parallel / syncretism (Mythographica rule).
3. **Provenance gates** — high/medium-confidence claims require sources; `citation_required` handling;
   developmental annotations require `asserted_by` + sources.
4. **Quality scores** — per-entity completeness/confidence scores; placeholder/orphan ratios.
5. **Automated audits** — scheduled jobs (generalize Mythographica `validate_graph.py`,
   `audit_graph_quality.py`); dashboards/alerts.
6. **Quality gates in the pipeline** — which failures block load vs. warn (ties to
   [../architecture/federation-and-ingestion.md](../architecture/federation-and-ingestion.md)).
7. **Review SLAs** — disputed/low-quality entity handling (ties to editorial governance).

## Existing assets to adopt

- Mythographica `validate_graph.py`, `audit_graph_quality.py`, per-node quality bar.

## Key decisions / open questions

- [ ] Hard-fail vs. quarantine for validation failures.

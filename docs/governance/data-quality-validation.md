# Data Quality & Validation

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the validation rules and quality gates that every record must pass before/within ingestion,
and the automated audits that monitor corpus health over time.

## Decided method (v1)

This is **stage [2] of the ingestion pipeline** — see
[federation-and-ingestion.md](../architecture/federation-and-ingestion.md). The gate runs three
check families in order; results route per [ADR-011](decision-log.md) (**quarantine, never drop**):

1. **Structural** *(hard — blocks the record)* — unique IDs, every relationship/claim endpoint
   resolves, schema + enum conformance, required fields present.
2. **Provenance** *(hard for high/medium confidence)* — `human_reviewed`+ claims and developmental
   annotations require `sources`; `citation_required` enforced; generator recorded.
3. **Epistemic** *(soft — down-rank + flag)* — `confidence ∈ [0,1]`; speculative links forced to low
   confidence; never equate linguistic cognate / functional parallel / syncretism (Mythographica
   rule). Violations don't drop the record — they cap its confidence and set a flag.
4. **Citation-support / entailment** *(for AI-authored writes — ADR-013)* — the cited source span must
   actually **support** the claim (NLI/entailment check by an independent verifier). This catches
   fabricated citations and citations that don't say what the claim says. The **support score becomes
   the claim's confidence**; below threshold → quarantine at `machine_unverified`. Specified in
   [../ai/rag-engineering.md](../ai/rag-engineering.md).

**Outcome routing:** structural/provenance failure → **quarantine** (with machine-readable reason);
epistemic failure → **load at reduced confidence + flag**; clean → continue to reconcile. A batch
partially succeeds; quarantined records are replayable after correction.

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

- [x] Hard-fail vs. quarantine → **quarantine** (ADR-011); structural/provenance block the record,
  epistemic issues down-rank rather than block.

# Evaluation & Success Metrics

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how we measure whether the corpus and the engine are good — data quality, federation
accuracy, and AI retrieval quality.

## Sections to detail

1. **Coverage** — entities/claims per tradition/module; gaps vs. a target ontology.
2. **Provenance health** — % of claims with sources; citation-required compliance; placeholder ratio.
3. **Reconciliation quality** — entity-resolution precision/recall on a labeled set; duplicate rate.
4. **Confidence calibration** — distribution of confidence; disputed-claim coverage.
5. **RAG quality** — retrieval precision/recall, citation faithfulness, hallucination rate,
   nuance-preservation (never asserts contested matters as fact).
6. **Developmental-layer quality** — annotation coverage, multi-reading representation, attribution rate.
7. **Reporting** — dashboards, periodic audits (ties to
   [../governance/data-quality-validation.md](../governance/data-quality-validation.md)).

## Key decisions / open questions

- [ ] Gold/eval datasets for reconciliation and RAG.

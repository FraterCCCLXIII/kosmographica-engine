# Evaluation & Success Metrics

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how we measure whether the corpus and the engine are good — data quality, federation
accuracy, and AI retrieval quality.

## Metrics & v1 targets

The numbers below are starting targets to steer quality, revised as the corpus grows. They feed the
periodic audits in
[../governance/data-quality-validation.md](../governance/data-quality-validation.md).

| Dimension | Metric | v1 target |
| --- | --- | --- |
| **Coverage** | entities/claims per tradition vs. a target ontology checklist | no tradition < 50% of its checklist |
| **Provenance** | % of `human_reviewed`+ claims with ≥1 source | 100% (hard gate) |
| **Provenance** | placeholder/orphan entity ratio | < 5% |
| **Reconciliation** | precision / recall on a labeled `sameAs` set | precision ≥ 0.95, recall ≥ 0.80 |
| **Reconciliation** | duplicate entity rate (post-resolution) | < 2% |
| **Confidence** | calibration: stated confidence vs. reviewer agreement | within ±0.15 |
| **Verifier** (ADR-013) | entailment accuracy on labeled supported/fabricated/misattributed set | ≥ 0.90; **false-publish < false-quarantine** |
| **RAG** | retrieval precision/recall; citation faithfulness | faithfulness ≥ 0.95 |
| **RAG** | hallucination / unsupported-assertion rate | < 1% |
| **RAG** | nuance preservation: never asserts contested matters as fact | 0 violations on the contested-claims probe set |
| **Developmental** | annotation coverage; multi-reading + attribution rate | attribution 100%; ≥ 2 readings where frameworks differ |

### Gold / eval sets (build alongside the pipeline)

- **Reconciliation gold** — hand-labeled same/different entity pairs (incl. the cross-tradition traps:
  Inanna/Ishtar, Hermes/Thoth) for entity-resolution scoring.
- **Verifier gold** — claims labeled supported / fabricated-source / misattributed, to track the
  ADR-013 verifier (its quality is the trust bottleneck).
- **RAG probe set** — questions with known contested answers, to test nuance preservation + citation
  faithfulness.

## Key decisions / open questions

- [x] Gold/eval datasets → **three labeled sets** (reconciliation, verifier, RAG probe) built with the pipeline.

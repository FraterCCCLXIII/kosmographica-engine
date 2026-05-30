# RAG & AI Retrieval Engineering

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).
> Engineering counterpart to the Religion & Mythology module §7 (chunking, GraphRAG).

## Purpose

Specify the retrieval engine: how entities become chunks + embeddings, how GraphRAG augments dense
retrieval with graph traversal, the answer-synthesis guardrails, the **claim verifier** that gates
AI writes (ADR-013), and the evaluation harness.

## Claim verifier (gates AI writes — ADR-013)

The publish-then-verify model lets AI write to canonical only if an **independent verifier** confirms
the cited source supports the claim. This is a retrieval/grounding problem, so it lives here.

1. **Inputs** — a staged claim + its cited source span(s) + the author model id.
2. **Entailment check** — an *independent* model (must differ from the author) judges whether the
   source span **entails / supports / contradicts / is-unrelated-to** the claim. Deterministic checks
   confirm the source exists in the registered corpus and the span is real (anti-fabrication).
3. **Score → confidence** — the support score becomes the claim's `confidence`; `contradicts` against
   an existing claim opens a dispute rather than writing.
4. **Outcome** — `support ≥ threshold` → write at `machine_validated`; else quarantine at
   `machine_unverified` (ties to [../governance/data-quality-validation.md](../governance/data-quality-validation.md) check 4).
5. **Continuous re-verification** — scheduled re-runs recompute confidence and decay stale claims.
6. **Verifier eval suite** — the verifier is a critical dependency; it needs its own labeled set
   (supported / fabricated / misattributed claims) tracked in the evaluation harness below.

## Sections to detail

1. **Chunking pipeline** — per-dimension chunks (module §7.1); chunk metadata (module §7.2);
   generation + refresh on entity change.
2. **Embeddings** — model choice(s), dimensionality, sparse tokens for hybrid search, re-embedding policy.
3. **Hybrid retrieval** — dense + sparse + reranker (module §7.3).
4. **GraphRAG traversal** — after seed retrieval, expand across relationship/claim/comparative/
   developmental edges; pull counter-claims; traversal depth/limits; ranking of traversed context.
5. **Answer synthesis & guardrails** — attribution-always; surface competing claims; never assert
   contested matters as fact (the Hermes↔Thoth pattern, module §14.6); developmental "answer at
   altitude" behavior; refusal/uncertainty handling.
6. **Prompt templates** — retrieval-to-answer templates with citation enforcement.
7. **Evaluation harness** — retrieval precision/recall, citation faithfulness, hallucination rate,
   nuance-preservation tests; regression set.
8. **Serving** — latency budget, caching, query API dependency (../architecture/api-contract.md).

## Key decisions / open questions

- [ ] Embedding model + vector store (ties to architecture).
- [ ] How deep GraphRAG traverses by default.
- [ ] Verifier model(s) + support-score threshold for `machine_validated` (ADR-013).

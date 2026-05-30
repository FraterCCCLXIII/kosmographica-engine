# RAG & AI Retrieval Engineering

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).
> Engineering counterpart to the Religion & Mythology module §7 (chunking, GraphRAG).

## Purpose

Specify the retrieval engine: how entities become chunks + embeddings, how GraphRAG augments dense
retrieval with graph traversal, the answer-synthesis guardrails, and the evaluation harness.

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

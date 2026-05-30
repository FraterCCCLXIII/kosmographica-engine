# Wave 2 Build Plan

> **Status:** ✅ shipped · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Builds directly on [Wave 1](./foundation-build-plan.md) (engine spine + AI write loop + read-only console).

## What shipped

| Stream | Delivered |
| --- | --- |
| **W2.1** | Provider-agnostic `LLMClient` (`kge/llm`: fake/Ollama/OpenAI-compatible) · `LLMAuthor` (drops non-verbatim quotes) · LLM/NLI verifier via `make_llm_verifier` behind the existing `Verifier(entailment=)` seam · swappable `Retriever` + `KeywordRetriever` (FTS + 1-hop) · gold eval set + `kge eval` baseline gate |
| **W2.2** | Sacred-Lineage adapter (stdlib-sqlite loader, partial-tolerant) · cross-source entity resolution (deterministic auto-link; name-block scoring → review; **no cross-tradition auto-merge on name**) · `Reconciliation` model + migration · non-destructive `sameAs` lifecycle + parity check · `/v1/reconcile/*` API + Console **Reconciliation** screen · `kge reconcile`/`parity` CLI. **Seeded live:** Sacred-Lineage = 1,809 entities / 1,177 relationships, converged |
| **W2.3** | `run_reverify` job emitting an audit delta · inline scheduler per ADR-005 (`kge worker --interval/--once`, `kge reverify`) using the configured verifier |
| **W2.4** | GitHub Actions CI (ruff + `alembic upgrade head` + pytest on a pgvector service; web eslint + tsc) · ruff config · `engine/.env.example` |

> **Live reconciliation note:** the two current sources cover near-disjoint subjects
> (Greek/Norse **deities** vs Buddhist/Hindu **figures**), so cross-source overlap is
> rare and the live queue is ~empty. The mechanism is proven by DB-backed tests; the
> queue grows as overlapping sources converge. **Embeddings + human action layer remain
> deferred to Wave 3** as decided. 56 engine tests pass.

## Where Wave 1 left off

Wave 1 proved the whole loop on **one** module with **deterministic stand-ins**:

- Ingestion, schema, tier-aware API, and the read-only Audit Console are real.
- The AI write loop runs end-to-end — but the **author** is a sentence-splitter and the **verifier** is a
  lexical-overlap heuristic. There is **no real retrieval** (embeddings unpopulated) and **one** source.

Wave 2 makes the thesis real: **trustworthy AI population at scale, across more than one source.**

## Primary objective

> Replace the stand-ins with a real **retrieval-grounded LLM author + LLM/NLI verifier** (gated by an eval
> suite; retrieval is keyword/graph-based with a swappable seam — vector backend deferred to Wave 3), and
> converge a **second source** through cross-source reconciliation — so the corpus grows by AI, stays
> auditable, and federates more than one dataset.

## Workstreams

### W2.1 — Real publish-then-verify (highest priority)

The verifier's entailment quality is the critical dependency called out in ADR-013; harden it first.
**Embedding/vector retrieval is deferred to Wave 3** — retrieval in Wave 2 is keyword/graph-based behind a
swappable seam, so the vector backend drops in later with no other code changes.

- **Swappable retrieval (`Retriever` interface):** define `retrieve(query, k) -> [SourceDoc/spans]`.
  Ship a **`KeywordRetriever`** (existing Postgres FTS `kge.search` + 1-hop graph expansion) now; a
  **`VectorRetriever`** (pgvector on the already-present `entities.embedding`) is a drop-in for Wave 3.
- **LLM-backed author** implementing the existing `Author` protocol: retrieve → propose claims **with
  verbatim source spans** (grounded; `requires_grounding=True`). No new write path — same envelope.
- **LLM/NLI verifier** behind the existing `Verifier(entailment=…)` seam: real entailment score replaces
  lexical overlap; keep the deterministic anti-fabrication + structural gate in front of it.
- **Eval suite (gate):** a gold set of (claim, source, label) pairs; measure verifier precision/recall and
  author grounding rate against [evaluation-metrics](./evaluation-metrics.md) targets. **The model swap
  only ships if it beats the lexical baseline on the gold set.**
- **Deliverables:** `kge/rag/` (Retriever interface + KeywordRetriever), real author + verifier adapters,
  `engine/evals/` + a `kge eval` command. **Acceptance:** ≥1 module re-verified by the LLM verifier; eval
  report committed; confidences reflect real entailment; vector retrieval is a documented TODO seam.
  **Specs:** [rag-engineering](../ai/rag-engineering.md), ADR-013.
- **Provider-agnostic:** author + verifier call a thin `LLMClient` interface (`complete`/`classify`), with
  config-selected adapters (hosted API **or** local Ollama) and a deterministic offline fake for tests/CI.
  No provider is pinned; pick the model at build time without touching call sites. (Embeddings deferred to Wave 3.)

### W2.2 — Second source: Sacred-Lineage adapter + cross-source reconciliation

First real test of **federation** (Wave 1 only had within-source idempotency).

> **Caveats (per source owner):** Sacred-Lineage's **data is incomplete** — treat it as a *partial,
> non-authoritative* contributor: ingest what exists, never assume coverage, and never let its gaps
> override Mythographica claims. Its **navigation/UI is explicitly not a reference model** — pull *data*
> from the repo, not interaction patterns; the Console/encyclopedia UX is designed independently.

- **Adapter:** `engine/src/kge/adapters/sacred_lineage.py` — Figure/Concept/Text/Practice → entities,
  Transmission/EntityLink → relationships + claims (per [migration-and-convergence](./migration-and-convergence.md) row c).
  Tolerate missing/partial fields gracefully (skip-and-log, don't fail the batch).
- **Cross-source entity resolution:** implement the [entity-resolution](../architecture/entity-resolution.md)
  matcher — deterministic external-id, then blocking + scoring → `sameAs` candidates. **Non-negotiables
  hold:** conflict → keep both claims; **no cross-tradition auto-merge on name alone**.
- **Reconciliation review queue + parity check:** surface proposed `sameAs` and run the `db:parity`-style
  row/coverage check before a source is "converged". (Parity is *consistency*, not completeness — partial
  source coverage is expected and fine.)
- **Deliverables:** adapter, `sameAs` lifecycle on `external_ids`/relationships, reconciliation API +
  Console screen. **Acceptance:** Sacred-Lineage ingested; overlapping figures (e.g. shared deities) linked
  via reviewed `sameAs`, not silently merged; parity passes.

### W2.3 — Continuous re-verification + background jobs (ADR-005)

- Move long work (embedding, verify, reverify) off the request path; a scheduler runs `reverify()` to
  recompute confidence, decay stale claims, and flag drift for spot-audit.
- **Deliverables:** a worker entrypoint + schedule (start synchronous/inline per ADR-005, add a queue only
  when forced). **Acceptance:** a scheduled re-verification run updates tiers/confidence and emits an audit delta.

### W2.4 — Operational hardening

- **CI:** GitHub Actions — lint + `pytest` (with a Postgres service) + `alembic upgrade head` check.
- **Config/secrets** for the LLM provider; `.env.example`. **Acceptance:** CI green on PRs.

## Sequencing

```text
W2.1 (real author/verifier + evals; swappable Retriever — vector deferred)  ──┐
W2.4 (CI) — in parallel, lightweight                                          ├─► W2.3 (re-verify scheduler)
W2.2 (Sacred-Lineage + cross-source reconciliation)  ─────────────────────────┘
```

W2.1 and W2.2 are independent and can run in parallel; W2.3 depends on W2.1's real verifier.

## Decisions

1. **Embedding/vector retrieval → deferred to Wave 3, built swappable.** ✅ decided. Wave 2 ships a
   `Retriever` seam with an FTS/graph implementation; the pgvector backend is a Wave 3 drop-in.
2. **Human action layer → deferred to Wave 3.** ✅ decided. Wave 2 is **AI-only**; humans still observe via
   the read-only Console. (Resolves with ADR-015 in Wave 3.)
3. **Second source → Sacred-Lineage.** ✅ decided. Imported as a *partial, non-authoritative* contributor
   (incomplete data tolerated; its navigation/UI is **not** a UX model). **time-thread is excluded** — its
   data is not reliably accurate.
4. **LLM provider → provider-agnostic.** ✅ decided. Author/verifier call a thin `LLMClient` interface with
   config-selected adapters (hosted API or local Ollama) + an offline fake for tests/CI; no model pinned now.

## Deferred to Wave 3

Embedding/vector (GraphRAG) retrieval backend · human action layer (auth + promote/reject/dispute) +
ADR-015 resolution · full NextWiki editorial/prose layer · Kosmotheon adapter · the developmental/altitude
lens (needs ADR-003/004) · public-facing encyclopedia UI · multi-tenant deployment.

**Excluded (not just deferred):** time-thread — its data is not reliably accurate, so it is not a federation
candidate until that's resolved upstream.

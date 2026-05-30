# Wave 2 Build Plan

> **Status:** proposed scope · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Builds directly on [Wave 1](./foundation-build-plan.md) (engine spine + AI write loop + read-only console).

## Where Wave 1 left off

Wave 1 proved the whole loop on **one** module with **deterministic stand-ins**:

- Ingestion, schema, tier-aware API, and the read-only Audit Console are real.
- The AI write loop runs end-to-end — but the **author** is a sentence-splitter and the **verifier** is a
  lexical-overlap heuristic. There is **no real retrieval** (embeddings unpopulated) and **one** source.

Wave 2 makes the thesis real: **trustworthy AI population at scale, across more than one source.**

## Primary objective

> Replace the stand-ins with a real **RAG-grounded author + LLM/NLI verifier** (gated by an eval suite),
> and converge the **second source (Sacred-Lineage)** through cross-source reconciliation — so the corpus
> grows by AI, stays auditable, and federates more than one dataset.

## Workstreams

### W2.1 — Real publish-then-verify (highest priority)

The verifier's entailment quality is the critical dependency called out in ADR-013; harden it first.

- **Embeddings & retrieval:** populate `entities.embedding` (and a claim/source text store) with a real
  embedding model; add a GraphRAG retrieval step (`kge.search` + vector ANN + 1-hop expansion).
- **LLM-backed author** implementing the existing `Author` protocol: retrieve → propose claims **with
  verbatim source spans** (grounded; `requires_grounding=True`). No new write path — same envelope.
- **LLM/NLI verifier** behind the existing `Verifier(entailment=…)` seam: real entailment score replaces
  lexical overlap; keep the deterministic anti-fabrication + structural gate in front of it.
- **Eval suite (gate):** a gold set of (claim, source, label) pairs; measure verifier precision/recall and
  author grounding rate against [evaluation-metrics](./evaluation-metrics.md) targets. **The model swap
  only ships if it beats the lexical baseline on the gold set.**
- **Deliverables:** `kge/rag/` (retrieval), real author + verifier adapters, `engine/evals/` + a
  `kge eval` command. **Acceptance:** ≥1 module re-verified by the LLM verifier; eval report committed;
  confidences now reflect real entailment. **Specs:** [rag-engineering](../ai/rag-engineering.md), ADR-013.
- **Decision needed:** LLM + embedding **provider** (hosted API vs. local) — see below.

### W2.2 — Second source: Sacred-Lineage adapter + cross-source reconciliation

First real test of **federation** (Wave 1 only had within-source idempotency).

- **Adapter:** `engine/src/kge/adapters/sacred_lineage.py` — Figure/Concept/Text/Practice → entities,
  Transmission/EntityLink → relationships + claims (per [migration-and-convergence](./migration-and-convergence.md) row c).
- **Cross-source entity resolution:** implement the [entity-resolution](../architecture/entity-resolution.md)
  matcher — deterministic external-id, then blocking + scoring → `sameAs` candidates. **Non-negotiables
  hold:** conflict → keep both claims; **no cross-tradition auto-merge on name alone**.
- **Reconciliation review queue + parity check:** surface proposed `sameAs` and run the `db:parity`-style
  row/coverage check before a source is "converged".
- **Deliverables:** adapter, `sameAs` lifecycle on `external_ids`/relationships, reconciliation API +
  Console screen. **Acceptance:** Sacred-Lineage ingested; overlapping figures (e.g. shared deities) linked
  via reviewed `sameAs`, not silently merged; parity passes.

### W2.3 — Continuous re-verification + background jobs (ADR-005)

- Move long work (embedding, verify, reverify) off the request path; a scheduler runs `reverify()` to
  recompute confidence, decay stale claims, and flag drift for spot-audit.
- **Deliverables:** a worker entrypoint + schedule (start synchronous/inline per ADR-005, add a queue only
  when forced). **Acceptance:** a scheduled re-verification run updates tiers/confidence and emits an audit delta.

### W2.4 — Minimal human action layer (scoped; full editorial still deferred)

Humans currently only observe. Add the **smallest** write surface that lets them act on the audit queue —
**without** committing to the full NextWiki editorial layer (ADR-015 stays open).

- **Auth + roles→scopes** (security-and-access): just enough to authorize promote/reject/dispute.
- **Human-action endpoints:** promote `machine_validated → human_reviewed`, reject (hide), open/resolve a
  dispute — all append-only/superseding (no overwrite), fully audited.
- **Console:** turn the read-only screens' detail views into actionable ones (behind auth).
- **Acceptance:** a reviewer can promote/dispute a claim; the action is an auditable superseding record.
- **Decision needed:** do this in Wave 2 or defer to Wave 3 (see below).

### W2.5 — Operational hardening

- **CI:** GitHub Actions — lint + `pytest` (with a Postgres service) + `alembic upgrade head` check.
- **Config/secrets** for the LLM provider; `.env.example`. **Acceptance:** CI green on PRs.

## Sequencing

```text
W2.1 (RAG + real author/verifier + evals)  ──┐
W2.5 (CI) — in parallel, lightweight          ├─► W2.3 (re-verify scheduler)
W2.2 (Sacred-Lineage + reconciliation)  ──────┘
W2.4 (human action layer) — last, or deferred to Wave 3
```

W2.1 and W2.2 are independent and can run in parallel; W2.3 depends on W2.1's real verifier; W2.4 depends on
W2.1/W2.2 producing things worth acting on.

## Decisions needed before building

1. **LLM/embedding provider** for W2.1 — hosted API (e.g. OpenAI/Anthropic + an embedding API) vs. local
   (Ollama + a local embedding model). Affects cost, secrets/CI, and offline-dev story.
2. **Human action layer (W2.4)** — include the minimal auth + promote/dispute surface in Wave 2, or keep
   Wave 2 AI-only and push all human-write to Wave 3 (resolving ADR-015 then).
3. **Confirm second source = Sacred-Lineage** (per convergence order) vs. **time-thread** (which would
   instead exercise the temporal/chronology spine sooner).

## Out of scope for Wave 2

Full NextWiki editorial/prose layer (ADR-015 resolution), time-thread + Kosmotheon adapters, the
developmental/altitude lens (needs ADR-003/004), public-facing encyclopedia UI, multi-tenant deployment.

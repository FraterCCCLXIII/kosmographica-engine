# Wave 3 Build Plan

> **Status:** proposed scope · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> Builds on [Wave 2](./wave-2-build-plan.md) (real publish-then-verify + a second federated source).

## Where Wave 2 left off

The corpus is real, federated (2 sources), AI-populated, and **auditable** — but only via the
internal **read-only Audit Console**. Nothing is public. Three things were explicitly deferred to
Wave 3: the **public-facing encyclopedia**, the **vector/embedding** retrieval backend, and the
**human action layer**.

## Primary objective

> **Make the trustworthy graph public.** Ship a fast, crawlable, **read-only public encyclopedia**
> (SSG/ISR) over the existing engine API — clamped to public tiers, every record **trust-badged**
> (ADR-013) — so a reader can browse, search, and explore the graph. Then light it up with semantic
> search/related (the deferred vector backend) and add the **human review layer** so experts can
> promote/adjudicate what the AI produced.

The public site is the headline deliverable; the other streams make it richer and trustworthy at scale.

## Workstreams

### W3.1 — Public encyclopedia app (headline)

A reader-facing surface per [frontend/app-architecture.md](../frontend/app-architecture.md) +
[frontend/design-system.md](../frontend/design-system.md). **Distinct audience from the Audit Console:**
polished, narrative, public-tier only.

- **Design system:** Tailwind + shadcn/ui driven entirely by **design tokens** (warm-canvas base from
  Sacred-Lineage `DESIGN.md`); serif display + humanist sans; light/dark; WCAG-AA. No hardcoded values.
- **Pages (SSG/ISR, server components):** landing/browse, **entity page** (`/{module}/{type}/{slug}`)
  with overview + sourced claims + relationships, and **search**. Every claim/entity shows its
  **trust-tier + confidence badge**; sacred/restricted gated; `machine_unverified` hidden by default
  (the API already clamps via `min_tier`).
- **Acceptance:** crawlable entity pages live for both sources, trust badges on every record, public
  tier clamp enforced, fast first paint (ISR). **Specs:** app-architecture, design-system, ADR-009/013.

### W3.2 — Slugs, stable public URLs & SEO

Public URLs must be human-readable and durable; KIDs stay the opaque internal identity.

- Mint stable **slugs** per entity (collision-safe), `slug → KID` resolution + redirects on change
  (identifiers-and-versioning.md), `sitemap.xml`, OpenGraph/meta. **Acceptance:** shareable
  `/{module}/{type}/{slug}` URLs that survive re-ingestion; KID still resolves.

### W3.3 — Graph Explorer island (D3)

The interactive payoff of a graph encyclopedia.

- Client island (D3, Mythographica precedent) around an entity using `/v1/entities/{kid}/graph`;
  level-of-detail + bounded traversal; node color by `type`, edge style by relation class.
  **Acceptance:** explore N-hop neighborhood from any public entity; linkable via query params.

### W3.4 — Vector retrieval backend (the deferred embedding drop-in)

Implements the Wave 2 `Retriever` seam's vector path — **no author/verifier changes**.

- Pluggable **embedding provider** (swappable like `LLMClient`); populate `entities.embedding`
  (already in schema) via an indexing job; add `VectorRetriever` (pgvector ANN) + a semantic
  `/search` mode and **"related entities"** on entity pages; use as the reconciliation tie-breaker.
  **Acceptance:** semantic search + related panel live; vector retriever passes the same grounding
  contract. **Decision:** embedding provider (hosted vs local). **Spec:** rag-engineering, entity-resolution.

### W3.5 — Human action layer + editorial UI (resolves ADR-015)

The deferred write surface — humans act on what the AI produced.

- **Auth + roles→scopes** (security-and-access). **Editorial actions** as contribution envelopes (no
  direct CRUD): promote `machine_validated → human_reviewed`, reject/hide, open/resolve disputes, and
  **adjudicate reconciliation** `sameAs` proposals — all append-only/superseding + audited.
- **Resolve ADR-015** (hybrid NextWiki vs from-scratch) for the editorial surface here.
  **Acceptance:** an authorized reviewer promotes/disputes a claim and accepts/rejects a `sameAs`; each
  is an auditable superseding record. **Specs:** security-and-access, ADR-015, entity-resolution.

## Sequencing

```text
W3.1 (public app) ──► W3.2 (slugs/SEO) ──► W3.3 (graph island)
W3.4 (vector backend) — parallel; enriches W3.1 search/related when ready
W3.5 (human layer + editorial) — parallel track; gated on auth, lands last
```

W3.1 is the critical path and ships first as a usable public site; W3.4 and W3.5 land incrementally.

## Decisions needed before building

1. **App topology** — extend the existing `web/` into **one app with route groups** (`(public)` +
   `(audit)`, per ADR-009) vs. a **separate public app** leaving the console as-is. *(Recommend: one
   unified app, route groups — coherent design system + API client.)*
2. **Scope of Wave 3** — public site **only** (W3.1–3.3) and push vector + human layer to Wave 4, or
   the **full** five-stream wave. *(Recommend: ship W3.1–3.3 first; W3.4/3.5 as fast-follows.)*
3. **Embedding provider** (if W3.4 included) — hosted API vs local; keep it swappable like the LLM.
4. **ADR-015** (if W3.5 included) — hybrid NextWiki vs from-scratch editorial UI.

## Deferred to a later wave

Kosmotheon adapter + the **developmental/altitude lens** (needs ADR-003/004) · media/archive surfaces ·
Comparison View / Comparative Mapping Engine · RAG Chat · Timeline Explorer · new modules (Phase 6) ·
multi-tenant deployment + sovereignty ops (Phase 7).

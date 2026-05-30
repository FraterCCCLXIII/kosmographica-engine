# Wave 3 Build Plan

> **Status:** W3.1–W3.3 shipped · W3.4–W3.5 pending · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
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

## Decisions (resolved)

1. **App topology → separate public app.** The public encyclopedia ships as its own read-optimized
   deployable (`site/`), distinct from the internal Audit Console (`web/`). This mirrors how
   Grokipedia separates its public reading site from its editorial/generation pipeline: different
   audiences, auth posture, freshness, and caching (public = SSG/ISR + CDN; console = always-fresh,
   internal). The public app is itself the "one unified app" of ADR-009 — it will absorb graph,
   compare, lens, and (behind auth) the editorial UI.
2. **Scope → site-first (W3.1–W3.3) now**; vector backend (W3.4) and human/editorial layer (W3.5) are
   fast-follows.
3. **Embedding provider** (W3.4) — TBD; swappable like the LLM client.
4. **ADR-015** (W3.5) — hybrid NextWiki vs from-scratch editorial UI; TBD.

## What shipped (W3.1–W3.3 · `site/`)

| Stream | Delivered |
|---|---|
| W3.1 | Public Next.js 16 app (`site/`): warm-canvas **design tokens**, landing/browse-by-type, **entity page** (`/{module}/{type}/{slug}`) with description, **cited + trust-rated claims**, connections; **search**. SSG/ISR; public tier clamp via the API. **Trust badges + confidence on every claim.** |
| W3.2 | Public **slugs** (`slugify(label)-<6hex KID>`) on `EntityOut` + `/v1/entities/by-slug/...` resolver (KID stays internal); `sitemap.xml` (202 URLs) + `robots.txt` + per-page OpenGraph/title metadata. |
| W3.3 | **D3 graph explorer** island on entity pages — force layout, node color by type, drag, keyboard-navigable, click to traverse. |

CI gains a `site` job (lint · typecheck · build). Engine API tests: 11 pass incl. slug + resolver.
Run locally: engine on `:8088`, `site` on `:3099`.

## Deferred to a later wave

Kosmotheon adapter + the **developmental/altitude lens** (needs ADR-003/004) · media/archive surfaces ·
Comparison View / Comparative Mapping Engine · RAG Chat · Timeline Explorer · new modules (Phase 6) ·
multi-tenant deployment + sovereignty ops (Phase 7).

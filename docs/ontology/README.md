# Kosmographica — Ontology Design Working Documents

> **Status:** active working area · **Date:** 2026-05-31
>
> This folder contains the design-stage ontology work for expanding and deepening Kosmographica's
> knowledge model — specifically the additions required to fulfill the mission of mapping human
> consciousness and development across religion, philosophy, myth, and the lives of sages.

## Documents in this folder

| Doc | Purpose | Status |
|---|---|---|
| [`gap-analysis.md`](./gap-analysis.md) | What the existing model covers well, what it's missing, and why | ✅ draft |
| [`motif-index-integration.md`](./motif-index-integration.md) | How to integrate the Thompson/ATU/Roud and related folk-motif index systems | ✅ draft |
| [`consciousness-mapping-layer.md`](./consciousness-mapping-layer.md) | The core mission layer: mapping human consciousness and development across all traditions | ✅ draft |
| [`philosophy-sage-lives-module.md`](./philosophy-sage-lives-module.md) | Ontology for the Philosophy & Science module, with deep treatment of philosophers' lives and lineages | ✅ draft |
| [`navigation-design.md`](./navigation-design.md) | How a user (or AI) navigates this graph — entry points, traversal axes, and UI implications | ✅ draft |
| [`cosmograph-catalog.md`](./cosmograph-catalog.md) | Catalog of 74 cosmographs — structured seed data + meta-taxonomy (`data/cosmographs/catalog.csv`) | ✅ draft |

## How this folder relates to the rest of the docs

These are **design and analysis documents** — upstream of the formal module specs in `docs/modules/`.
Once design decisions here are settled, they flow downstream:

- Ontology decisions → `docs/modules/philosophy-science.md` (to be written)
- Motif index decisions → `docs/modules/religion-mythology.md` (to be extended)
- Consciousness mapping decisions → `docs/core-meta-model.md` §4 (developmental layer extension)
- Navigation decisions → `docs/frontend/app-architecture.md`
- Cosmograph catalog → `docs/modules/philosophy-science.md` · religion-mythology cosmology entities

## The mission statement this work serves

> Map human consciousness and development — across every tradition, framework, period, and geography
> — in a single, claim-based, provenance-first knowledge graph that a human can browse and an AI can
> reason over.

The three moves that make this possible:

1. **Motif as node, not tag.** Mythological motifs (flood, dying god, world tree, initiatory
   descent) are first-class entities that traditions, texts, and figures *relate to* — not metadata
   labels attached to stories.
2. **Consciousness as traversable axis.** Every entity can be annotated with where it sits in
   the space of human development (stages, states, lines, quadrants) — not as a single truth but as
   a set of competing scholarly interpretations, each a claim with confidence and sources.
3. **Lives as narrative + graph.** The "life of a philosopher/sage" is not a biography record; it
   is a structured cluster of entities and claims — teachers, encounters, texts produced, concepts
   coined, lineages founded — that can be traversed, compared, and searched.

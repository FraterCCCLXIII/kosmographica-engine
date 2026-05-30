# Kosmographica — Architecture Review

> Review of `religion_knowledge_graph_spec.md` (v1.1) in light of the broader Kosmographica
> vision and the existing sibling datasets it is meant to federate.
>
> **Status:** discussion draft · **Date:** 2026-05-29

---

## 1. Mission framing

Kosmographica's stated goal is a **total record of human thought, culture, and development, and total
history — through an integral developmental lens.** The current spec is, by its own title, a
*World Religion & Mythology Knowledge Graph*. It is an excellent comparative-religion design, but it
was written in isolation from the four production datasets it is supposed to unify, and it
under-delivers on the mission in two decisive ways:

1. **Scope** — it is scoped to religion & mythology, not to the full record of human thought,
   culture, and history.
2. **The integral developmental lens is absent** — the one dimension that distinguishes Kosmographica
   from "another religion wiki" is not modeled at all.

This document records what the landscape actually is, what the spec gets right, and the
highest-leverage improvements. The companion document
[`kosmographica-core-meta-model.md`](./kosmographica-core-meta-model.md) proposes the concrete schema.

---

## 2. The datasets Kosmographica must federate

These sibling repos are not loose examples — they are the layers the engine must integrate, and
**three of them already implement large parts of what the spec proposes from scratch**.

| Repo | What it really is | Already implements |
|---|---|---|
| **Interpretatio-Universalis** (titled *"Mythographica"*) | Comparative mythology graph, React + FastAPI + Postgres | The spec's claim model (edges = **assertions**: `confidence` 0–1, `methodology`, `sources`, `explanation`) and most of the comparative-predicate vocabulary (`linguistic_cognate` vs `functional_parallel` vs `syncretic_identification` — the exact "don't collapse nuance" concern) |
| **Sacred-Lineage** (*Kechimyaku-2*) | Guru/disciple transmission chains, Next.js + Prisma | A large slice of the entity ontology: `Tradition/School/LineageChart`, `Figure`, `TransmissionRelationship`, `RelationshipType` (with `inverseKey`/`direction`), a polymorphic `EntityLink` (`certainty`, `citation`, `startYear/endYear`), plus `Concept`, `Text`, `Practice`, `Institution`, `Place`, `HistoricalPeriod`, `Event` |
| **Kosmotheon** | The **integral developmental lens** (Wilber AQAL, Spiral Dynamics, Gebser, Vervaeke; Wilber–Combs lattice, states & stages) | The entire developmental dimension the spec is missing |
| **time-thread-web** | Historical timeline spine (World History Timeline) | The temporal/chronological backbone |
| **Panentheon / Panentheism** | Meta-religious synthesis essays + a large glossary | *Reference only — see note below; not an authority* |

> **Note on Panentheon.** Its vocabulary layer (`interpretatio-universalis.md`,
> `iconotheca-universalis`) is **incomplete and potentially inaccurate** and must **not** be adopted as
> Kosmographica's controlled vocabulary. At most it may serve as an informal pointer for terms to
> investigate, every one of which must be independently verified against primary/scholarly sources
> before entering the graph. The controlled vocabulary should be built fresh (see §4.6).

### 2.1 The core structural problem

The spec **reinvents** the claim model (Mythographica) and the entity ontology (Sacred-Lineage) as
greenfield designs, with divergent field names, ID conventions, and confidence encodings:

- Mythographica: numeric `confidence` (0.0–1.0), camelCase fields, `snake_case` string IDs (`norse_odin`).
- Spec: enum `confidence_level`, a UUID-keyed base schema.
- Sacred-Lineage: integer IDs, a polymorphic `EntityLink` with `certainty` + year bounds.

Left unreconciled, Kosmographica inherits **three incompatible "claim" models**. Reconciliation —
not more ontology — is the highest-value architectural work.

---

## 3. What the spec gets right

- **Claim-based, not fact-based** (§3.3, §15) — the central insight, and correct. It already matches
  Mythographica's production "assertion" model.
- **Comparative-relationship layer** (§14) — typed, time-bounded, tradition-scoped edges with
  similarities/differences and multi-claim dispute handling. Genuinely ahead of most religion DBs.
- **Provenance & confidence everywhere** (§11.2) — the right default posture.
- **RAG chunk strategy** (§5/§7) — per-dimension chunking with structured metadata is well-judged.
- **Place as meaning-cluster with multi-layer significance** (§5) — the right model for contested sites.

These should be preserved. The recommendations below extend rather than replace them.

---

## 4. Highest-leverage improvements

### 4.1 Reframe: federated core + domain modules

The doc is `religion_knowledge_graph_spec`, but the repo is `kosmographica-engine` and the mission is
total. Restructure as:

- **A thin universal core** — every entity, regardless of domain, is a node carrying: identity, `Claim[]`,
  `Relationship[]`, `Source[]`, a **temporal anchor**, a **spatial anchor**, and a **developmental
  annotation** (§4.2). This is the spec's universal entity schema generalized one level up.
- **Domain modules** that extend the core: *Religion & Mythology* (what the spec already is, and the
  best-developed), then *Philosophy & Science*, *Art & Culture*, *Polity & Society*, *Technology*.
  The current 26 entity types become the type set of the Religion & Mythology module.

This lets the existing spec stand as a domain module while making room for "total record" without a rewrite.

### 4.2 Add the Integral / Developmental layer (the missing thesis)

This is the most important addition. The spec has "Experience State" (samādhi/satori) but **no
developmental stages/altitudes** — yet the developmental lens is the whole reason Kosmographica
exists, and Kosmotheon already holds the content. It must be first-class **and claim-based** (a
developmental reading of a tradition is an interpretation, not a fact — exactly the epistemics the
spec already champions). Add:

- **`DevelopmentalFramework`** entity (AQAL, Spiral Dynamics, Gebser, Fowler, Kohlberg, …).
- **`DevelopmentalStage` / `Altitude`** entities with **cross-framework mapping**
  (archaic → magic → mythic → rational → pluralistic → integral; SD beige → turquoise) — exactly
  Kosmotheon's "By Stage" axis.
- A **developmental annotation** attachable to *any* entity/claim/text/practice/movement, carrying
  `framework_id`, `altitude`, `state` (the Wilber–Combs **state × stage** distinction), `quadrant`
  (AQAL interior/exterior × individual/collective), plus `confidence` + `sources` + `asserted_by`.
  Treat it as a sibling layer to the Claim and Comparative layers.
- AI payoff: "present multiple developmental readings" / "answer at the questioner's altitude" — a
  differentiator no religion database has.

### 4.3 Make the Claim model *one* model, adopted from Mythographica

Declare Mythographica's assertion schema (entities + assertions; `confidence` ∈ [0,1], `methodology`,
`sources`, `explanation`) the **canonical claim implementation**, and reconcile the spec's
enum-based `confidence_level` to it (store a numeric score *and* a derived band). Source the
comparative-predicate vocabulary from Mythographica's existing, battle-tested `relationType` list
rather than defining a parallel one.

### 4.4 Add a federation / entity-resolution layer

Nothing in the spec explains how the same deity in Mythographica, time-thread, and Sacred-Lineage
becomes one node. Add:

- A **canonical Kosmographica URI/ID scheme** plus a **`sameAs` / reconciliation** table mapping each
  source-system ID (Mythographica `norse_odin`, Sacred-Lineage `Figure.id`, Wikidata `Q…`) to the
  canonical entity.
- **`source_system` provenance** on every imported record.
- An **ingestion pipeline** that orchestrates the existing seed/normalize scripts
  (Mythographica `seed_from_json.py`, Sacred-Lineage `db:import-legacy`) rather than replacing them.

### 4.5 Strengthen the temporal spine + add bitemporality

"Total history" needs more than `date_range` + a `circa` bool. Make **`HistoricalPeriod`/`Era`**
first-class (Sacred-Lineage already has it; PeriodO is the external authority), represent
**contested/fuzzy dating as claims**, treat the **time-thread** timeline as the canonical chronology,
and add **bitemporality** (valid-time vs. transaction-time) so the "as understood in century X"
slider actually works. Tie macro-historical period schemes (Big History, Gebser's cultural
structures) back to the developmental layer.

### 4.6 Build the controlled vocabulary fresh — do **not** reuse Panentheon

The spec invokes SKOS but points at no actual thesaurus. **Do not adopt Panentheon's glossary**
(incomplete / potentially inaccurate). Instead, build the controlled vocabulary/SKOS concept scheme
**fresh**, anchored on the already-guardrailed **Mythographica tradition & relation taxonomy**
(`meta.traditionTaxonomy`, `edgeTypeGuide`, the `comparative-methodology.md` epistemic rules), and
extend it under the same per-term quality bar (definition + sources + confidence). Treat any external
glossary as an unverified lead, not a load source.

### 4.7 Smaller but worth adding

- **Cultural sovereignty / ethics layer** — indigenous traditions are already in scope (Andean,
  Caribbean, Celtic expansions exist in Mythographica). Add **CARE principles + Traditional Knowledge
  (TK) Labels** and sacred/restricted-content handling alongside the existing CIDOC/IIIF standards.
- **Identifiers for the broader scope** — VIAF (persons), Pleiades (ancient places),
  Getty AAT/ULAN (art/iconography), PeriodO (periods) — enables "total record" interoperability.
- **GraphRAG** — the RAG section is vector-centric; add graph-traversal-augmented retrieval since a
  graph store is already mandated.

---

## 5. Priority ordering

| Priority | Improvement | Why now |
|---|---|---|
| P0 | Federated core + domain modules (§4.1) | Everything else hangs off the framing |
| P0 | Integral/developmental layer (§4.2) | The defining thesis; currently absent |
| P0 | One canonical claim model (§4.3) | Prevents three incompatible claim schemas |
| P1 | Entity resolution / federation (§4.4) | Required to merge the existing datasets |
| P1 | Temporal spine + bitemporality (§4.5) | "Total history" + the time-aware UI |
| P2 | Fresh controlled vocabulary (§4.6) | Needed for SKOS export; build, don't borrow |
| P2 | Ethics/sovereignty, identifiers, GraphRAG (§4.7) | Hardening and interop |

---

## 6. Proposed deliverables

1. **This review** — `docs/ARCHITECTURE_REVIEW.md`.
2. **The core meta-model** — [`docs/kosmographica-core-meta-model.md`](./kosmographica-core-meta-model.md):
   the thin universal core, the domain-module mechanism, the developmental layer schema, the
   reconciled claim model, and the federation/entity-resolution design.
3. *(Optional, later)* reframe `religion_knowledge_graph_spec.md` as the **Religion & Mythology
   domain module** that conforms to the core meta-model.

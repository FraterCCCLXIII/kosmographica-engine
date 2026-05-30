# Kosmographica — Core Meta-Model

> The thin universal core, the domain-module mechanism, the integral/developmental layer, the
> reconciled claim model, and the federation/entity-resolution design that lets the existing
> datasets (Mythographica, Sacred-Lineage, Kosmotheon, time-thread) compose into one graph.
>
> **Status:** discussion draft · **Date:** 2026-05-29 · **Companion:** [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md)

---

## 0. Design principles

1. **Everything is an entity with typed, provenanced relationships.** (Inherited from the spec.)
2. **Store claims, not facts.** Every contestable assertion is a first-class `Claim` with confidence
   and sources. (Inherited from the spec; aligned to Mythographica's production assertion model.)
3. **Thin core, fat modules.** The core defines only what is universal across all of human thought,
   culture, and history. Domain knowledge lives in modules that extend the core.
4. **The developmental lens is structural, not cosmetic.** Any node or claim can be annotated with a
   developmental reading, and those readings are themselves claims.
5. **Federate, don't re-key.** Existing datasets keep their native IDs; the core maps them via a
   reconciliation layer. Kosmographica orchestrates ingestion; it does not fork the source schemas.
6. **Bitemporal and source-attributed.** Every record knows *when it was true* and *when/where we
   recorded it*.

---

## 1. Layer overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  DOMAIN MODULES                                                       │
│  Religion & Mythology · Philosophy & Science · Art & Culture ·        │
│  Polity & Society · Technology · …                                    │
│  (each adds entity subtypes + module-specific relationship types)     │
├─────────────────────────────────────────────────────────────────────┤
│  CROSS-CUTTING LAYERS (apply to every entity in every module)         │
│   • Claim layer            (provenanced assertions)                   │
│   • Comparative layer      (typed cross-entity equivalences)          │
│   • Developmental layer    (integral / AQAL / stage annotations)      │
│   • Temporal layer         (eras, bitemporal validity)                │
│   • Spatial layer          (places, geometry, significance)           │
│   • Media layer            (IIIF image records)                       │
│   • RAG layer              (chunks + embeddings)                      │
├─────────────────────────────────────────────────────────────────────┤
│  UNIVERSAL CORE                                                       │
│   Entity · Relationship · Claim · Source · DevelopmentalAnnotation ·  │
│   TemporalAnchor · SpatialAnchor                                      │
├─────────────────────────────────────────────────────────────────────┤
│  FEDERATION                                                           │
│   Canonical IDs · sameAs reconciliation · source_system provenance ·  │
│   ingestion pipeline                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Universal core

### 2.1 `Entity`

The minimal node shared by every module. Domain modules add a `subtype` vocabulary and extension
fields; they do not change the core.

```
entity {
  id                : KID                      // canonical Kosmographica ID, see §6
  module            : ModuleType               // religion_mythology | philosophy_science | art_culture | polity_society | technology | core
  type              : EntityType               // module-scoped (e.g. Deity, Text, Person, Work, Movement, Concept, Place, Event)
  subtype           : string[]
  canonical_name    : string
  alternate_names   : { name, language, script, kind }[]   // kind: transliteration | epithet | regional | historical
  short_description : string                   // <= 280 chars; graph labels + RAG summaries
  long_description  : string

  // cross-cutting anchors (all optional, all claim-backed where contestable)
  temporal          : TemporalAnchor?          // see §5
  spatial           : SpatialAnchor[]          // see module / spec §5
  developmental     : DevelopmentalAnnotation[]// see §4

  // cross-cutting collections
  relationships     : Relationship[]           // see §2.2
  claims            : Claim[]                   // see §3
  comparative_edges : ComparativeRelationship[]// see spec §14
  sources           : Citation[]
  media             : ImageRecord[]            // see spec §6
  rag_chunks        : RAGChunk[]               // see spec §7

  // status & quality
  status            : living | historical | reconstructed | disputed | mythic | symbolic
  source_quality    : primary | secondary | tertiary | oral | archaeological

  // federation & interop
  source_system     : SourceSystem             // see §6
  external_ids      : ExternalId[]             // wikidata, viaf, geonames, pleiades, getty_ulan, periodo, …
  uri               : IRI                       // dereferenceable canonical URI

  // editorial / bitemporal
  recorded_at       : datetime                 // transaction-time
  last_reviewed     : date?
  editor_notes      : string?
}
```

> **Migration note.** The spec's `tradition_ids`, `region_ids`, `texts`, etc. become typed
> `Relationship[]` entries rather than bespoke fields, so the core stays domain-agnostic. Modules may
> still expose them as convenience views.

### 2.2 `Relationship`

Directional, typed, qualified, provenanced. The predicate vocabulary is **sourced from Mythographica's
existing `relationType` list** plus Sacred-Lineage's `RelationshipType` (which already carries
`direction` and `inverseKey`).

```
relationship {
  id           : KID
  subject_id   : KID
  predicate    : RelationshipType   // controlled; carries direction + inverse_key
  object_id    : KID
  qualifiers   : { date_range?: DateRange, region?: string, context?: string }
  methodology  : linguistic | textual | functional | iconographic | syncretic | archaeological | developmental
  confidence   : float              // 0.0–1.0 (canonical); see §3.3 for band derivation
  sources      : Citation[]
  notes        : string?
}
```

---

## 3. Claim layer (reconciled, single model)

Kosmographica adopts **Mythographica's assertion model** as the one canonical claim implementation.
The spec's enum `confidence_level` is reconciled by storing **both** a numeric score and a derived band.

### 3.1 `Claim`

```
claim {
  id            : KID
  subject_id    : KID
  predicate     : string
  object        : KID | literal

  claim_type    : historical | mythological | doctrinal | hagiographic | traditional
                | archaeological | scholarly | comparative | developmental | symbolic | folk | disputed

  // confidence — canonical numeric + derived band (kept in sync)
  confidence        : float          // 0.0–1.0   (canonical, from Mythographica)
  confidence_band   : high | medium | low | tradition_specific | contested | speculative | unknown  // derived

  methodology   : linguistic | textual | functional | iconographic | syncretic | archaeological | developmental
  explanation   : string             // 1–2 sentences, scholarly tone (Mythographica convention)

  // provenance
  source_ids            : KID[]
  secondary_source_ids  : KID[]
  tradition_id          : KID?       // which tradition makes the claim
  asserted_by           : string[]

  // scope
  date_range        : DateRange?
  region            : string[]?
  tradition_context : string?

  // dispute
  is_disputed       : boolean
  counter_claim_ids : KID[]
  dispute_notes     : string?

  // editorial / bitemporal
  citation_required : boolean
  reviewed_by       : string?
  review_date       : date?
  recorded_at       : datetime       // transaction-time
}
```

### 3.2 Confidence reconciliation

| Source encoding | Maps to canonical `confidence` | `confidence_band` |
|---|---|---|
| Mythographica `confidence` 0.0–1.0 | identity | banded by thresholds below |
| Spec `confidence_level: high` | 0.85 | high |
| Spec `medium` | 0.6 | medium |
| Spec `low` | 0.35 | low |
| Spec `traditional_only` | n/a (numeric) | tradition_specific |
| Spec `speculative` | ≤ 0.4 | speculative |
| Spec `disputed` | n/a (numeric) | contested |
| Sacred-Lineage `certainty` (string) | mapped per lookup | per lookup |

Banding thresholds (tunable): `≥0.8 high · 0.55–0.79 medium · 0.3–0.54 low · <0.3 speculative`.
`tradition_specific` and `contested` are orthogonal flags derived from `claim_type`/`is_disputed`,
not from the numeric score.

---

## 4. Developmental (integral) layer

The defining Kosmographica layer, currently absent from the spec. Content already exists in
Kosmotheon (AQAL, Spiral Dynamics, Gebser, Vervaeke, the Wilber–Combs lattice). Every developmental
reading is a **claim** (interpretive and contestable), so it carries confidence + sources.

### 4.1 `DevelopmentalFramework`

```
developmental_framework {
  id          : KID
  name        : string            // "AQAL", "Spiral Dynamics", "Gebser structures", "Fowler stages of faith", …
  author_ids  : KID[]             // links to Person entities (Wilber, Beck, Gebser, …)
  description : string
  axes        : DevelopmentalAxis[]   // e.g. stages, states, lines, quadrants
}
```

### 4.2 `DevelopmentalStage` (altitude) with cross-framework mapping

```
developmental_stage {
  id            : KID
  framework_id  : KID
  name          : string          // "mythic", "rational", "pluralistic", "integral"; SD "blue", "orange", "green", "teal"
  ordinal       : int             // sequence within the framework
  altitude      : string          // shared cross-framework altitude key (archaic|magic|mythic|rational|pluralistic|integral|…)
  equivalents   : KID[]           // stages in other frameworks claimed-equivalent (claim-backed)
  description   : string
}
```

The shared `altitude` key is what enables the Kosmotheon "By Stage" axis to align Spiral Dynamics,
Gebser, Fowler, etc. Cross-framework `equivalents` are themselves comparative claims, never asserted
as identity.

### 4.3 `DevelopmentalAnnotation` (attachable to any entity or claim)

```
developmental_annotation {
  id            : KID
  target_id     : KID             // any Entity or Claim
  framework_id  : KID
  stage_id      : KID?            // altitude / structure-stage  (vertical axis)
  state         : gross | subtle | causal | nondual | null   // Wilber–Combs state (horizontal axis)
  quadrant      : UL | UR | LL | LR | null    // AQAL: interior/exterior × individual/collective
  line          : string?         // developmental line (cognitive, moral, spiritual, aesthetic, …)

  // because a developmental reading is an interpretation, it is claim-grade:
  confidence    : float
  asserted_by   : string[]        // which interpreter/school makes this reading
  sources       : KID[]
  notes         : string?
}
```

> **Why state × stage is kept distinct:** the Wilber–Combs lattice shows a mystical *state* can be
> accessed at any *stage* but is interpreted through that stage's structure. Collapsing them is the
> classic category error; the schema enforces the separation.

---

## 5. Temporal layer

```
temporal_anchor {
  date_range    : DateRange       // { start, end, circa: bool, bce: bool }
  precision     : exact | decade | century | period | mythic | unknown
  period_ids    : KID[]           // links to HistoricalPeriod / Era entities (PeriodO-aligned)
  calendar      : string?         // source calendar system; normalized to proleptic Gregorian ISO
  dating_claims : KID[]           // contested datings represented as Claims, not a single value
}
```

- **`HistoricalPeriod` / `Era`** are first-class entities (Sacred-Lineage already models this), the
  canonical chronology is the **time-thread** timeline, and contested dates are **claims**, not a
  `circa` bool.
- **Bitemporality:** entities/claims carry `recorded_at` (transaction-time) while `date_range`
  encodes valid-time, enabling "as understood in century X" queries and the spec's time-aware
  similarity slider.
- Macro-historical schemes (Big History, Gebser cultural structures) link to the **developmental
  layer** via `DevelopmentalStage.altitude`.

---

## 6. Federation & entity resolution

### 6.1 Canonical IDs and URIs

- **KID** — canonical Kosmographica ID, e.g. `kg:entity/<uuid>`; dereferenceable as
  `https://kosmographica.org/id/<uuid>` (JSON-LD / RDF).
- Every entity keeps its **`source_system`** and native key; the canonical KID is the join target.

### 6.2 `sameAs` reconciliation

```
reconciliation {
  kid            : KID
  source_system  : mythographica | sacred_lineage | kosmotheon | time_thread | manual | …
  source_id      : string          // native key: "norse_odin" | Figure.id | doc path | timeline event id
  match_method   : exact | curated | embedding | wikidata_bridge
  confidence     : float
  reviewed_by    : string?
}

external_id {
  kid       : KID
  authority : wikidata | viaf | geonames | pleiades | getty_ulan | getty_aat | periodo | cts_urn
  value     : string
}
```

The same deity in Mythographica (`norse_odin`), a Sacred-Lineage `Figure`, a time-thread event, and
Wikidata `Q…` collapse to one KID via these tables — without re-keying the source systems.

### 6.3 Ingestion pipeline

Kosmographica **orchestrates** existing loaders rather than replacing them:

| Source | Native artifact / loader | Into core via |
|---|---|---|
| Mythographica | `{meta,nodes,edges}` JSON · `seed_from_json.py` · `/import/json` | node→Entity, edge→Claim/Relationship, taxonomy→vocabulary |
| Sacred-Lineage | Prisma/SQLite · `db:import-legacy` | Figure→Entity, TransmissionRelationship→Relationship, EntityLink→Claim |
| Kosmotheon | MkDocs markdown | prose→long_description + DevelopmentalFramework/Stage extraction |
| time-thread | timeline JSON | events→Event entities + canonical chronology |

Pipeline stages: **extract → normalize (camelCase/field map) → reconcile (sameAs) → load → validate
(epistemic rules) → index (graph + vector + search).**

---

## 7. Domain modules

A module = an entity-subtype vocabulary + module-specific relationship/claim types, all extending the
core. No module may redefine core fields.

| Module | Status | Representative entity types |
|---|---|---|
| **Religion & Mythology** | Specified ([`modules/religion-mythology.md`](./modules/religion-mythology.md)) | the existing 26 types |
| **Philosophy & Science** | To design | Person, Work, Theory, Field/Discipline, School, Argument |
| **Art & Culture** | To design | Work (art/music/literature), Movement, Genre, Style, Artist |
| **Polity & Society** | To design | Polity, Institution, Event, Movement, Law, Office |
| **Technology** | To design | Invention, Technique, Artifact, Infrastructure |

The Religion & Mythology spec is reframed (later) as the first module that **conforms to** this core:
its base entity schema becomes a profile of §2.1, its claim schema a profile of §3, its comparative
layer unchanged, plus the developmental layer (§4) layered on top.

---

## 8. Controlled vocabulary

Built **fresh** — Panentheon's glossary is **not** adopted (incomplete / potentially inaccurate). The
SKOS concept scheme is anchored on **Mythographica's already-guardrailed taxonomy**
(`meta.traditionTaxonomy` with `family` / `tradition` / `subtradition`, the `edgeTypeGuide`, and the
`comparative-methodology.md` epistemic rules) and extended under the same per-term quality bar:
every term needs a definition, sources, and a confidence/quality rating before it enters the graph.
External glossaries (including Panentheon's) are treated as **unverified leads to investigate**, never
as load sources.

---

## 9. Cross-cutting standards & ethics

- **Linked data:** RDF / JSON-LD export, dereferenceable KID URIs, SPARQL endpoint.
- **Cultural heritage:** CIDOC CRM (entity integration), IIIF (images), SKOS (vocabulary).
- **Sovereignty & ethics:** **CARE principles** and **Traditional Knowledge (TK) Labels** for
  indigenous and living traditions; sacred/restricted-content flags with access controls. This is a
  first-class requirement, not an afterthought, given the indigenous traditions already in scope.
- **Retrieval:** hybrid vector + sparse + **GraphRAG** (graph-traversal-augmented retrieval over the
  relationship/claim/developmental layers).

---

## 10. Open questions

1. Canonical store: extend Mythographica's Postgres assertion store, or stand up a dedicated core DB
   that all systems sync into? (Affects whether reconciliation is push or pull.)
2. Do domain modules get their own graph namespaces, or one graph with `module` as a node label?
3. Altitude key: adopt an existing cross-framework scale (e.g. Wilber's altitude colors) as the
   canonical `altitude`, or define a Kosmographica-neutral scale and map each framework to it?
4. How much of Kosmotheon's prose becomes structured entities vs. linked long-form `Article` records?

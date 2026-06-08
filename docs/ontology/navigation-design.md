# Navigation Design — Traversing the Knowledge Graph

> **Status:** draft · **Date:** 2026-05-31
> **Upstream:** `docs/ontology/gap-analysis.md` §2.4
> **Downstream:** `docs/frontend/app-architecture.md`
> **Purpose:** Design the semantic navigation layer — how a human (or AI) enters and traverses
> this graph productively without already knowing what they're looking for.

---

## 1. The navigation problem

A graph of 500,000+ entities is only useful if there are well-designed entry points and traversal
paths. Without this, the graph is a database that experts query and general users cannot find
their way around.

The navigation design answers three questions:

1. **Where can you start?** (Entry points — the "front doors")
2. **How do you move through the graph?** (Traversal axes — the dimensions of exploration)
3. **How does the UI make this feel natural?** (Information architecture — page design)

---

## 2. Entry points — the front doors

There are six primary ways a user arrives at content. Each requires a distinct landing experience.

### 2.1 By tradition / religion

The most intuitive entry for most users. "I want to explore Buddhism" or "I want to understand
what Sufism teaches about the soul."

Landing page shows:
- Tradition entity (short description, key claims, temporal span)
- Sub-traditions / schools / lineages as a collapsible tree
- Key figures (founders, major teachers, saints)
- Core texts
- Core concepts and doctrines
- Practices and rituals
- Sacred places
- Developmental annotation: what altitude is this tradition's primary expression? (with caveats)

This entry point serves the *tradition-centric* explorer.

### 2.2 By concept or idea

"What is nirvāṇa?" or "How do different traditions think about sacrifice?" or "What is the
relationship between logos and dharma?"

Landing page shows:
- Concept entity (canonical definition, short description)
- Tradition-specific interpretations (ConceptInterpretation entities)
- Texts that articulate it
- Figures associated with it
- Related concepts (presupposes, contradicts, elaborates, analogous_to)
- Motifs associated with it
- Developmental annotation: at what stage does this concept typically appear?

This entry point serves the *concept-driven* researcher.

### 2.3 By figure / person

"Tell me about Nagarjuna" or "What do we know about Pythagoras?" or "Who were Rumi's teachers?"

Landing page shows:
- Person entity (birth/death, tradition affiliation, biographical summary)
- Teacher-student chain (lineage visualization — upstream and downstream)
- Works authored / attributed
- Key concepts coined or developed
- Schools founded or joined
- Places associated with
- Developmental annotation
- Source quality indicator: how much of this is historical vs. hagiographic?

This entry point serves the *biographical* explorer and the lineage researcher.

### 2.4 By motif

"Show me all traditions that have a flood myth" or "What cultures have the dying-and-rising god
motif?" or "Where does the world-tree appear?"

Landing page shows:
- MotifEntry entity (TMI code, definition, category)
- All texts and traditions where it is attested (instantiates_motif relationships)
- Geographic distribution (map view)
- Temporal distribution (timeline view)
- Related motifs (parent, children, clusters_with)
- Developmental annotation: what stage does this motif typically operate at?
- Narrative meta-framework readings (Propp function, Campbell stage, if applicable)

This entry point serves the *comparative mythologist* and the consciousness-mapper.

### 2.5 By developmental stage

"Show me everything in the database that is annotated at the mythic-rational transition" or
"What practices across all traditions are associated with the subtle state?"

Landing page shows:
- Stage entity (altitude key, framework, description)
- All entities annotated at this stage (filtered by entity type: persons, texts, practices,
  concepts, motifs)
- Cross-framework equivalents at this stage
- Navigation to adjacent stages (one above, one below)
- Featured traversal: "What does the transition FROM this stage look like?"

This entry point serves the *integral / developmental* researcher — the core audience for the
consciousness-mapping mission.

### 2.6 By text / scripture

"I want to explore the Upanishads" or "What is the Zohar and how does it relate to the Torah?"

Landing page shows:
- Text entity (title, author/attribution, date, tradition)
- Canonical status (canonical_in relationships)
- Commentaries on this text
- Texts this text comments on
- Key concepts expressed in it
- Figures associated with its composition, transmission, and interpretation
- Motifs it contains (instantiates_motif)
- Manuscript / source quality information

---

## 3. Traversal axes — the dimensions of exploration

Once a user is at an entity, they can traverse along any of these axes. The UI presents these as
tabs, panels, or linked sections on the entity page.

### Axis 1: Tradition axis
*"Stay within this tradition, go deeper or broader"*

From any entity: → parent tradition → sub-traditions → sibling entities within the same tradition

### Axis 2: Conceptual axis
*"Follow the idea — what does it connect to intellectually?"*

From a concept: → presupposes → elaborates → contradicts → expressed_in → related concepts
From a text: → concepts it contains → arguments it makes → concepts it coins

### Axis 3: Biographical / lineage axis
*"Follow the people — who taught whom?"*

From a person: → teachers → students → school founded → contemporaries → influenced_by

### Axis 4: Comparative / cross-traditional axis
*"Where does this appear elsewhere?"*

From any entity: → equivalent_in (other traditions) → analogous_to → identified_with (by tradition)
→ same motif in other cultures → same concept under different names

### Axis 5: Temporal axis
*"When did this emerge and how did it develop?"*

From any entity: → time-thread era → preceded_by → derived_from → later developments
→ "what was happening in the world when this emerged?"

### Axis 6: Developmental / consciousness axis
*"Where does this sit in the map of human development?"*

From any entity: → developmental annotations → stage → equivalent entities at same stage
→ entities at adjacent stages → state annotations → Wilber-Combs lattice position

### Axis 7: Motif / narrative axis
*"What story patterns does this participate in?"*

From a myth, text, or figure: → instantiated motifs → tale types → related motifs
→ cross-cultural attestations of same motif

### Axis 8: Spatial axis
*"Where in the world does this live?"*

From any entity with spatial anchors: → map view → related places → pilgrimage routes
→ other traditions at the same place (Jerusalem as shared site)

---

## 4. The entity page template

Every entity page, regardless of type, follows this structure. Sections that have no data for
a given entity are hidden (not shown as empty).

```
[Entity Page Template]

HEADER
  canonical_name  (+ alternate names, expandable)
  type badge  |  tradition badge(s)  |  period badge
  short_description (≤280 chars)
  source quality indicator  (primary / secondary / hagiographic / etc.)
  confidence band (for the entity's core claims)

BODY — tabbed or sectioned:

  Tab: Overview
    long_description (encyclopedic)
    key claims (top 5, with confidence indicators)
    developmental annotation summary (stage + state + framework name)

  Tab: Relationships
    grouped by family (Tradition / People / Texts / Concepts / Practices / Places / Motifs)
    each relationship shown as: [predicate] → [linked entity card] (confidence + source)
    comparative relationships highlighted separately

  Tab: Claims
    full claim list, filterable by:
      claim_type (historical / doctrinal / hagiographic / comparative / developmental)
      confidence band
      asserted_by (tradition)
      disputed (yes/no)
    each claim expandable to show sources, methodology, counter-claims

  Tab: Texts & Sources
    primary sources that concern this entity
    secondary literature
    manuscript / archaeological notes

  Tab: Developmental
    full developmental annotation(s) with framework, stage, state, quadrant, line
    competing annotations from different scholars
    "What does this look like from a different framework?" — cross-framework view
    link to Stage entity landing page

  Tab: Media
    IIIF images, manuscript pages, iconography
    sacred sites (map)

  Tab: Graph View
    D3 force-directed graph of immediate neighborhood (depth 1–3)
    filterable by relationship family
    navigable (click a node to go to that entity page)

FOOTER
  External links: Wikidata, VIAF, Pleiades, Perseus, JSTOR, etc.
  Provenance: source_system, recorded_at, last_reviewed, editor_notes
  Cite this entity: auto-generated citation in multiple formats
```

---

## 5. Special navigation views

Beyond the entity page, several special views serve the consciousness-mapping mission.

### 5.1 The Stage Panorama

A full-page view of one developmental stage (e.g., "Mythic"):

- All entity types annotated at this stage, shown as cards in groups: Traditions / Figures /
  Concepts / Practices / Motifs / Texts
- Filter by tradition, geography, period
- Side panel: cross-framework equivalents at this stage
- Navigation: ← previous stage | next stage →
- "Transition zone" view: entities annotated at the boundary between this stage and the next

### 5.2 The Lineage Tree

A dedicated visualization for teacher-student chains and transmission lineages:

- Start from any figure or lineage entity
- Expand upstream (teachers) or downstream (students, successors)
- Annotate nodes with: dates, key works, tradition, developmental stage
- Highlight lineage breaks (where transmission was disputed or interrupted)
- Cross-tradition view: show parallel lineages in different traditions on the same timeline

### 5.3 The Motif Atlas

A geographic and temporal map of motif attestations:

- Select a motif (e.g., A1010 "Flood")
- Map view: dots where this motif is attested, colored by tradition family
- Timeline view: earliest attestation to latest
- Cluster view: which other motifs co-occur with this one most frequently?
- Stage view: at what developmental stages does this motif appear, and how does its meaning shift?

### 5.4 The Concept Genealogy

A specialized traversal view for tracing a concept's development through time:

- Start node: a concept or term
- Traverse: derived_from, anticipated, influenced_by, synthesized, translates
- Timeline axis: earliest expression → latest
- Stage axis: developmental annotation at each node
- Cross-tradition axis: how the concept migrated between traditions

This is the view that answers the consciousness genealogy queries in `consciousness-mapping-layer.md` §6.

### 5.5 The Comparative Table

A side-by-side view for comparing how multiple traditions handle the same concept or motif:

```
Concept: "Self / Soul / Ātman"

| Tradition      | Name         | Definition                          | Relationship to Ultimate | Stage |
|----------------|--------------|-------------------------------------|--------------------------|-------|
| Advaita Vedanta| Ātman        | Identical to Brahman                | Is Brahman               | integral |
| Buddhism       | Anātman      | No permanent self                   | Contradicts the concept  | rational |
| Christianity   | Soul         | Individual, immortal, created       | Subordinate to God       | mythic-rational |
| Islam          | Nafs         | Self / soul with stages of purif.   | Returns to Allah         | mythic-rational |
| Jainism        | Jīva         | Eternal individual soul             | Distinct from matter     | mythic-rational |
| Samkhya        | Puruṣa       | Pure consciousness, distinct        | Distinct from Prakṛti    | rational |
```

The comparative table is generated dynamically from ConceptInterpretation entities.

---

## 6. AI navigation layer

The knowledge graph is also navigated by AI (RAG queries, GraphRAG traversal). The navigation
design for AI differs from human navigation:

**Chunk strategy:** Each entity page section (overview, claims, relationships, developmental)
becomes a distinct RAG chunk with its entity metadata as structured context. This allows the AI
to retrieve a *claim* without retrieving the full entity, and to traverse relationships
programmatically.

**GraphRAG traversal:** For queries like "explain the relationship between Neoplatonism and
Islamic philosophy," the AI traverses: Plotinus → influenced_by chain → Porphyry → Iamblichus
→ Arabic translations → al-Kindi → al-Farabi → Ibn Sina, assembling a path-coherent narrative.

**Developmental queries:** For "what does ego dissolution look like at different stages," the AI
queries `DevelopmentalAnnotation` entities filtered by a state flag (non-dual / ego dissolution)
and groups results by `altitude`, then assembles a comparative narrative.

**Confidence-aware responses:** The AI is instructed to report confidence bands when summarizing
claims, and to flag hagiographic vs. scholarly sources. A claim with `confidence: 0.3` and
`methodology: hagiographic` should be presented differently from one with `confidence: 0.85`
and `methodology: textual`.

---

## 7. Navigation anti-patterns to avoid

**Anti-pattern 1: The religion directory.** Navigation that forces users to pick a religion first,
then drill down, makes cross-traditional and concept-first exploration impossible. All six entry
points must be equally prominent.

**Anti-pattern 2: The flat list.** Listing 500 entities under "Buddhism" without sub-grouping by
type, period, or stage makes the tradition landing page useless. Sub-groupings must be
meaningful and consistent.

**Anti-pattern 3: The confidence black hole.** Showing claims without confidence indicators
creates false certainty. Every claim display, at every level, must surface at least the confidence
band (high / medium / low / contested).

**Anti-pattern 4: Stage as label.** Showing a developmental stage annotation as a simple label
("this is a Mythic tradition") without surfacing the scholarly claims behind it, the competing
annotations, and the caveat that this is an interpretation not a fact — collapses the nuance the
system is built to preserve.

**Anti-pattern 5: Dead ends.** Every entity page must have at least one navigable outgoing edge
to a related entity. Orphan nodes should be flagged for editorial attention, not silently displayed.

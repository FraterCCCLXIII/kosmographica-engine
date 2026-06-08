# Gap Analysis — Existing Ontology vs. the Full Mission

> **Status:** draft · **Date:** 2026-05-31
> **Purpose:** Identify what the current Kosmographica model handles well, where the gaps are,
> and what must be added to fully serve the mission of mapping human consciousness and development.

---

## 1. What the existing model does well

The `core-meta-model.md` + `religion-mythology.md` module together establish a genuinely strong
foundation. These are the parts we should not redesign:

**Claim-first provenance.** Every contestable assertion is a `Claim` with numeric confidence
(0.0–1.0), methodology, sources, and dispute tracking. This is exactly right — it is what separates
a knowledge graph from an encyclopedia.

**Entity model breadth.** The religion-mythology module covers 26+ entity types: traditions,
persons, texts, concepts, practices, places, symbols, cosmologies, experience states, motifs, and
stances (including atheism/critique). This is unusually comprehensive.

**Developmental layer.** The `DevelopmentalAnnotation` schema — stage, state, quadrant, line —
is architecturally correct. Keeping state × stage separate (the Wilber–Combs lattice) is the right
move and rare in the field.

**Federation design.** The `sameAs` reconciliation layer, KID minting, and `source_system`
provenance mean that Mythographica, Sacred-Lineage, Kosmotheon, and time-thread can compose without
re-keying.

**Mythological Motif as entity type.** The religion-mythology module already names `Mythological
Motif` as a first-class entity type. This is the correct instinct — it just needs to be fully
specified (see `motif-index-integration.md`).

---

## 2. Gaps — what is missing or underdeveloped

### 2.1 The motif index systems are unmodeled

The Thompson Motif Index (TMI), the Aarne–Thompson–Uther (ATU) tale-type index, and the
many culture-area indices (Irish, Arab, Polynesian, etc.) are enormous structured classification
systems used by comparative folklorists for a century. They represent the closest thing to a
universal grammar of narrative that scholarship has produced.

The current ontology names `Mythological Motif` as an entity type but gives it no:
- Classification axis mapping to the TMI/ATU taxonomy
- Schema for the motif itself (code, category, definition, culture attestations)
- Relationship vocabulary for how a text, myth, or tradition *instantiates* a motif
- Coverage of tale-type vs. motif distinction (a tale type is a recurring plot; a motif is a
  recurring narrative element — they nest, but they are not the same)

See `motif-index-integration.md` for the full design.

### 2.2 The Philosophy & Science module is a stub

`docs/modules/philosophy-science.md` exists as a placeholder. For the consciousness-mapping mission,
this is the second most important module after religion-mythology — philosophers, arguments, schools,
and the *lives of thinkers* are central data.

Missing:
- Entity types for Argument, Theory, Field/Discipline, Concept-as-philosophical-object (distinct
  from religious concept), Thought Experiment, Aphorism
- The "lives of philosophers" tradition (Diogenes Laertius, Porphyry, Iamblichus, Plutarch,
  hagiographic biographies) as a distinct source type with its own epistemics
- Relationship types for philosophical succession (taught_by, founded_school_of, refuted,
  synthesized_with, anticipated, rehabilitated)
- The distinction between a philosopher's *reported* views and their *actual* views (both are
  claims, but with different methodology flags)

See `philosophy-sage-lives-module.md` for the full design.

### 2.3 The consciousness-mapping layer is architecturally present but content-empty

The developmental layer schema (§4 of core-meta-model.md) is well-designed, but:
- The `DevelopmentalFramework` entities (AQAL, Spiral Dynamics, Gebser, Fowler, etc.) are not yet
  populated or specified with enough depth to be usable
- There is no design for how cross-framework mapping works at query time — how do you ask "show me
  all entities at the mythic-rational transition across all frameworks simultaneously"?
- The `altitude` key (the shared cross-framework ordinal) is defined but the actual key values and
  their mappings to each framework are not specified
- Phenomenological and contemplative frameworks (Husserl, Varela's neurophenomenology, the
  Tibetan phenomenology of the bardos, etc.) are not modeled — these are essential for mapping
  *states* rather than *stages*

See `consciousness-mapping-layer.md` for the full design.

### 2.4 Navigation and traversal are underspecified

The frontend and app-architecture docs exist but the *semantic* navigation design — what are the
primary entry points into this graph for a human who doesn't already know what they're looking for —
is not designed. For a graph of this scope, navigation design is as important as ontology design:
a user arriving at "reincarnation" should be able to traverse to:
- Every tradition's version of the concept (Concept Interpretation entities)
- The developmental stage at which this belief typically appears
- The motifs associated with it (world-reversal, life-after-death, initiatory death)
- The philosophers and sages who wrote about it
- The experience states (near-death, samādhi) that traditions associate with it

This traversal structure needs to be explicitly designed, not left to the UI team to infer.

See `navigation-design.md` for the full design.

### 2.5 The hagiographic / biographical source type is underspecified

Texts like Diogenes Laertius's *Lives of the Eminent Philosophers*, Plutarch's *Lives*,
Porphyry's *Life of Plotinus*, Iamblichus's *Life of Pythagoras*, the Pali *Thera/Therīgāthā*,
the Chinese *Jingde Chuandeng Lu* (lamp records), Islamic *tabaqāt* (biographical dictionaries),
and Hindu hagiographies like the *Bhaktamāla* are a distinct class of source.

They are:
- Partial and tendentious (written to construct a lineage or teaching, not to report facts)
- Essential (often the only record of a thinker's life and milieu)
- Structurally mythologized (miraculous birth, divine encounter, death-scene teachings)

The current model treats these as `Text / Scripture` or `Commentary` entities, which loses the
distinct epistemics. A hagiographic source needs its own `source_quality` flag and methodology.

### 2.6 Narrative structure meta-frameworks are absent

Beyond motif indexes, there are several scholarly meta-frameworks for understanding narrative
structure that belong in the ontology as `ScholarlyTheory` entities:
- Vladimir Propp's morphology of the folktale (31 functions, 8 character spheres)
- Joseph Campbell's monomyth / hero's journey
- Northrop Frye's archetypal criticism (comedy, tragedy, romance, satire)
- René Girard's mimetic theory / scapegoat mechanism
- Walter Burkert's Greek religion / ritual killing framework
- Georges Dumézil's trifunctional hypothesis (Indo-European)

These are not just texts — they are *interpretive frameworks* that can be applied to myth/narrative
entities as `ScholarlyTheory` claims, generating comparative annotations across the database.

---

## 3. Priority order for filling the gaps

| Gap | Priority | Rationale |
|---|---|---|
| Motif index integration | P0 | Foundational to the myth/narrative layer; blocks comparative work |
| Philosophy module + sage lives | P0 | Core mission; second major domain after religion-mythology |
| Consciousness-mapping layer depth | P1 | Architecturally present; needs content specification |
| Navigation design | P1 | Blocks frontend work; high leverage |
| Hagiographic source epistemics | P1 | Needed for both religion and philosophy modules |
| Narrative meta-frameworks | P2 | Important but can be added incrementally as `ScholarlyTheory` entities |

---

## 4. What NOT to change

- The claim model. Numeric confidence + band + sources + dispute is correct.
- The developmental layer architecture. State × stage separation is correct.
- The federation design. KID + sameAs + source_system is correct.
- The entity types in religion-mythology.md. They are comprehensive; we extend, not replace.
- The CARE principles / TK Labels requirement. Non-negotiable.

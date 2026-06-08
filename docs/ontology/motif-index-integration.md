# Motif Index Integration Design

> **Status:** draft · **Date:** 2026-05-31
> **Upstream:** `docs/ontology/gap-analysis.md` §2.1
> **Downstream:** `docs/modules/religion-mythology.md` (extension)

---

## 1. The scholarly landscape

The comparative study of myth and folklore has produced several large, structured classification
systems. These are not competing — they layer on top of each other and address different levels
of narrative structure.

### 1.1 The primary systems

**Thompson Motif Index (TMI)** — Stith Thompson, *Motif-Index of Folk-Literature* (1932–1936,
rev. 1955–1958). The foundational system. ~46,000 motifs organized into 23 top-level categories
(A–Z), each hierarchically subdivided. A motif is a "smallest element in a tale having a power to
persist in tradition" — it can be a character (A0–A99: Creator), an item (D800–D899: Magic objects),
or an incident (F0–F199: Other-world journeys). The TMI is motif-level; it does not organize
whole plots.

**Aarne–Thompson–Uther Index (ATU)** — Hans-Jörg Uther, *The Types of International Folktales*
(2004), updating Aarne (1910) and Thompson (1961). Classifies ~2,500 tale *types* — recurring
whole-plot structures, each assigned a number (ATU 300 = "The Dragon Slayer", ATU 510A =
"Cinderella"). A tale type is a bundle of motifs in a recognized sequence. The ATU is plot-level;
the TMI is element-level.

**Roud Folk Song Index** — Steve Roud, ~25,000 entries. Classifies traditional English-language
folk songs by tune/text family. Orthogonal to ATU/TMI; applies mainly to song tradition.

**Culture-area indices** — Many parallel indices exist for regions not covered or under-covered by
Thompson: Irish (Cross 1952), Arab (El-Shamy 1995), Polynesian (Kirtley 1971), Balkan Slavic
(Kristić 1984), Arthurian French (Guerreau-Jalabert 1992), Thousand and One Nights (El-Shamy 2006),
etc. These use TMI notation but add culture-specific motifs.

**DUCHAS / Irish Folklore Commission** — digitized Irish folklore archive at duchas.ie; indexed
using the ATU system.

**Frenzel (world literature motifs)** — Elisabeth Frenzel, *Motive der Weltliteratur* (1976–) —
extends motif analysis to canonical literary texts, not just folk tradition.

### 1.2 Key conceptual distinctions

| Concept | Definition | Example |
|---|---|---|
| **Motif** | Smallest persistent narrative element | K1000 "Deception into self-injury"; B11 "Dragon" |
| **Tale type** | Recognized whole-plot bundle of motifs | ATU 300 "Dragon Slayer" |
| **Motif instance** | A specific occurrence of a motif in a text or tradition | The flood in Genesis = motif A1010 |
| **Cross-cultural attestation** | The set of cultures/texts where a motif appears | A1010 attested in 200+ traditions |
| **Motif complex** | A cluster of functionally related motifs that co-occur | Initiatory-death cluster: F80+E1+D1960 |

---

## 2. Entity model for motif integration

The existing `Mythological Motif` entity type in religion-mythology.md is correct as a starting
point. We extend it with a full schema.

### 2.1 `MotifEntry` entity (extends core `Entity`)

```
motif_entry {
  // Core entity fields (id, canonical_name, etc.)
  
  // Classification
  motif_system    : tmi | atu | roud | cross | frenzel | culture_area | local
  motif_code      : string          // e.g. "A1010", "ATU 300", "Roud 9"
  motif_category  : string          // TMI top-level letter (A=Mythological, B=Animals, ...)
  parent_motif_id : KID?            // hierarchical parent in the index
  child_motif_ids : KID[]           // more specific motifs under this one

  // Definition
  canonical_definition : string     // Thompson's or Uther's definition verbatim (with citation)
  scholarly_notes      : string     // additional context, debate, boundary cases

  // Attestation (handled via Relationships + Claims, not a field)
  // use: attested_in → Text/Tradition/Culture entities
  
  // Cross-system mapping
  equivalent_motif_ids : KID[]      // same motif in a different index (claim-backed)
  atу_type_ids         : KID?[]     // if a tale type, which ATU number(s)
  
  // Structural
  propp_function   : string?        // Propp's 31 morphological functions (if applicable)
  campbell_stage   : string?        // Hero's Journey stage (if applicable)
  
  // Developmental annotation (inherited from core)
  // developmental : DevelopmentalAnnotation[]
}
```

### 2.2 `TaleType` entity (extends core `Entity`)

A tale type is a distinct entity from a motif — it is a whole-plot structure.

```
tale_type {
  // Core entity fields
  
  atu_number      : string          // e.g. "ATU 300"
  aarne_number    : string?         // older Aarne number if different
  title           : string          // e.g. "The Dragon Slayer"
  summary         : string          // plot summary
  
  // Component motifs
  core_motifs     : KID[]           // MotifEntry entities that define this type
  optional_motifs : KID[]           // motifs that appear in some versions
  
  // Distribution
  primary_culture_area : string[]   // where this tale type is most common
  attested_in          : KID[]      // specific texts/traditions (via Relationship)
}
```

### 2.3 New relationship types for motif integration

Add to the religion-mythology module's relationship vocabulary:

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `instantiates_motif` | Text/Myth/Narrative → MotifEntry | This text contains an instance of this motif |
| `exemplifies_tale_type` | Text/Myth/Narrative → TaleType | This text is an instance of this tale type |
| `has_variant_in` | MotifEntry → Tradition/Text | A culture-specific variant of the motif |
| `clusters_with` | MotifEntry → MotifEntry | Motifs that regularly co-occur (not hierarchical) |
| `transforms_into` | MotifEntry → MotifEntry | Lévi-Straussian transformation (same structure, inverted values) |
| `refines` | MotifEntry → MotifEntry | More specific version (sub-motif relationship) |
| `composed_of` | TaleType → MotifEntry | The tale type includes this motif |

---

## 3. TMI category hierarchy as a classification axis

The TMI's 23 top-level categories form a natural classification axis for the Religion & Mythology
module — analogous to how the developmental layer provides a stage axis. Every Myth/Narrative entity
should be taggable with the TMI categories its motifs fall under.

| TMI Category | Code | Relevance to consciousness-mapping mission |
|---|---|---|
| Mythological motifs | A | Creation, cosmogony, cultural origins — maps to archaic/magic stages |
| Animals | B | Transformation, totem, divine animal — magic-mythic transition |
| Taboo | C | Prohibition and consequence — mythic-rational boundary |
| Magic | D | Transformation, objects of power — magic/mythic |
| The dead | E | Afterlife, resurrection, ancestor — cross-stage |
| Marvels | F | Other worlds, supernatural feats — cross-stage |
| Ogres | G | Devouring, chaos, shadow — mythic |
| Tests | H | Initiation, proof of worthiness — mythic-rational |
| The wise and the foolish | J | Wisdom literature, aphorism — rational |
| Deceptions | K | Trickster logic — cross-stage |
| Reversal of fortune | L | Humility/pride, low-becoming-high — mythic-rational |
| Ordaining the future | M | Prophecy, fate — mythic |
| Chance and fate | N | Luck, coincidence — |
| Society | P | Social structure, kingship — |
| Rewards and punishments | Q | Moral consequence — mythic-rational |
| Captives and fugitives | R | Captivity, escape — |
| Unnatural cruelty | S | Sacrifice, abandonment — mythic |
| Sex | T | Sacred marriage, fertility — magic-mythic |
| Traits of character | W | Vice and virtue — rational-pluralistic |
| Humor | X | Comic tales — |
| Religion | V | Worship, prayer, sacred — all stages |
| Miscellaneous | Z | Formulas, meta-narrative | |

---

## 4. Integration strategy with existing datasets

### 4.1 Immediate integration targets

**folkmasa.org** — provides a browsable TMI. We import the motif hierarchy as `MotifEntry`
entities with `source_system: tmi_thompson` and `external_ids` pointing to the TMI code. This is
a read-only reference import — it does not create attestation claims, only the motif vocabulary.

**ATU Index** — import the ~2,500 tale types as `TaleType` entities from Uther's published index.

**Mythographica** — the existing Mythographica JSON already has myth/narrative nodes and edge types.
The ingestion pipeline adds a reconciliation pass: for each narrative node, attempt motif-code
matching and create `instantiates_motif` relationships as claims (confidence proportional to match
method: exact TMI code = 0.9, semantic match = 0.5).

**DUCHAS (duchas.ie)** — Irish Folklore Commission archive uses ATU numbers. Where DUCHAS records
are ingested as Text entities, their ATU numbers flow directly into `exemplifies_tale_type`
relationships.

### 4.2 AI-assisted motif annotation

A key use of the AI authoring workflow (see `docs/ai/ai-authoring-workflow.md`) is automated
motif annotation: given a Myth/Narrative entity with a `long_description`, the AI proposes
candidate TMI motifs as `instantiates_motif` claims with confidence < 0.7, pending human review.
This is the scalable path to covering the full corpus.

### 4.3 What we are NOT doing

We are not building our own motif index — Thompson and Uther's work is the standard. We reference
their codes as external identifiers, the same way we reference Wikidata Q-numbers or VIAF IDs.
Culture-area indices (El-Shamy, Cross, Kirtley, etc.) are added as additional `motif_system`
values with the same pattern.

---

## 5. Consciousness-mapping relevance

Motifs are not just folkloristic curiosities — they are evidence for recurring patterns in human
imagination across developmental stages. Several motif clusters map directly to the
consciousness-mapping mission:

**Initiatory death and rebirth** (TMI E0–E99, D1960, F80): the most widely attested cross-cultural
motif cluster. Appears in shamanic initiation (archaic/magic), mystery religions (mythic), Sufi
annihilation (pluralistic), and integral non-dual traditions. Tracing this motif across stages
is one of the primary value propositions of the database.

**World-tree / axis mundi** (TMI A652): cosmological centering principle. Maps to the
mythic-rational transition — the point where spatial cosmology begins to be read as inner topology.

**Trickster** (TMI J1700–J2800, K0–K999): the figure who breaks rules to reveal their arbitrariness.
Developmental readings span from magic (raw transgression) to pluralistic (deconstruction of
fixed identity).

**Divine marriage / hieros gamos** (TMI T100–T199): sacred union as cosmological principle.
Developmental readings from fertility magic through alchemical coniunctio to non-dual integration.

**The descent to the underworld** (TMI F80–F109): initiatory katabasis. Orpheus, Inanna, Persephone,
Aeneas, Dante. Maps to the encounter with shadow / unconscious at every stage.

These clusters should be tagged explicitly with `developmental_annotation` entities, making them
traversable by stage in the UI.

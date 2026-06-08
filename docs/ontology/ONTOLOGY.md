# Kosmographica — Complete Ontology

> **Status:** living document · **Version:** 0.2 · **Date:** 2026-05-31
>
> Single consolidated ontology for Kosmographica — the knowledge graph for a total record of
> human thought, culture, and development through an integral developmental lens.
>
> **Governing principle:** Where this document and `docs/core-meta-model.md` conflict, the core
> meta-model governs. This document extends and specifies; it does not replace.
>
> **How to iterate:** Edit this document directly. Record significant decisions in
> `docs/governance/decision-log.md`. When a section stabilizes it flows downstream into the
> formal module spec under `docs/modules/`.
>
> **Changelog v0.1 → v0.2:**
> - Collapsed §3/§4 redundancy: §3 is now the single authoritative entity listing; §4 is a module-ownership map
> - Added `ConceptInterpretation` schema (§3.3)
> - Added `Narrative` entity distinct from `Text` (§3.2)
> - Added `Symbol` as a first-class semiotic entity with its own schema (§3.2)
> - Added `TransmissionEvent` entity (§3.4)
> - Dissolved Family J; predicates absorbed into correct families
> - Added `reinterprets`, `opposes`, `embodies` relationships
> - Added `respect` qualifier to `equivalent_in`
> - Fixed `disputed` removed from `claim_type` (it is a state, not a type)
> - Committed `attribution_claim` pattern and meta-claim documentation (§6)
> - Expanded altitude table with genre and practice columns (§7.5)
> - Fixed Sufi maqāmāt: stations in stage frameworks, states in state frameworks (§7.1, §7.2)
> - Committed answer to stage-rejection annotation pattern (§7.8, was Open Question 5)
> - Added experience state as seventh navigation entry point (§15.1)
> - Fixed teacher_of / student_of redundancy in Family F

---

## Table of Contents

1. [Mission & Design Principles](#1-mission--design-principles)
2. [Architecture Overview](#2-architecture-overview)
3. [Entity Type Catalogue](#3-entity-type-catalogue)
   - 3.0 Tradition Structure
   - 3.1 Agents
   - 3.2 Expressions (Texts · Narratives · Symbols · Practices · Material)
   - 3.3 Ideas & Concepts (incl. ConceptInterpretation schema)
   - 3.4 Space, Time & Events (incl. TransmissionEvent schema)
   - 3.5 Claims
4. [Module Ownership Map](#4-module-ownership-map)
5. [Relationship Taxonomy](#5-relationship-taxonomy)
   - Family A: Tradition Hierarchy
   - Family B: Transmission & Influence
   - Family C: Textual
   - Family D: Conceptual
   - Family E: Cross-Traditional (Comparative)
   - Family F: Membership, Role & Lineage
   - Family G: Space-Time & Practice
   - Family H: Epistemic (Claims)
   - Family I: Motif & Narrative
6. [The Claim Model](#6-the-claim-model)
7. [The Developmental / Consciousness-Mapping Layer](#7-the-developmental--consciousness-mapping-layer)
   - 7.1 Stage frameworks (incl. Sufi stations)
   - 7.2 State frameworks (incl. Sufi states)
   - 7.3 Lines of development
   - 7.4 Quadrants
   - 7.5 Altitude key with genre & practice columns
   - 7.6 The Wilber–Combs lattice as query structure
   - 7.7 DevelopmentalAnnotation schema
   - 7.8 Annotating traditions that reject stage models
8. [The Motif Index Layer](#8-the-motif-index-layer)
9. [The Biographical / Hagiographic Layer](#9-the-biographical--hagiographic-layer)
10. [Comparative Layer](#10-comparative-layer)
11. [Temporal Layer](#11-temporal-layer)
12. [Spatial Layer](#12-spatial-layer)
13. [Controlled Vocabulary & Classification Axes](#13-controlled-vocabulary--classification-axes)
14. [Federation & Entity Resolution](#14-federation--entity-resolution)
15. [Navigation Design](#15-navigation-design)
16. [Implementation Notes](#16-implementation-notes)
17. [Open Questions](#17-open-questions)

---

## 1. Mission & Design Principles

### Mission

> Map human consciousness and development — across every tradition, framework, period, and
> geography — in a single, claim-based, provenance-first knowledge graph that a human can browse
> and an AI can reason over.

### The three moves that make this possible

**Motif as node, not tag.** Mythological motifs (flood, dying god, world tree, initiatory descent)
are first-class entities that traditions, texts, and figures *relate to* — not metadata labels.
This enables cross-cultural pattern queries: "show me every tradition that has the initiatory
death motif, sorted by developmental stage."

**Consciousness as traversable axis.** Every entity can be annotated with where it sits in the
space of human development (stages, states, lines, quadrants) — not as a single truth but as a
set of competing scholarly interpretations, each a claim with confidence and sources.

**Lives as narrative + graph.** The "life of a philosopher or sage" is not a biography record;
it is a structured cluster of entities and claims — teachers, encounters, texts produced, concepts
coined, lineages founded — that can be traversed, compared, and searched.

### Design principles

1. **Everything is an entity with typed, provenanced relationships.** No information is embedded
   in unstructured text that cannot be queried.
2. **Store claims, not facts.** Every contestable assertion is a first-class `Claim` with numeric
   confidence (0.0–1.0), methodology, sources, tradition context, and dispute tracking.
3. **Thin core, fat modules.** The core defines only what is universal. Domain knowledge lives in
   modules that extend the core without redefining it.
4. **The developmental lens is structural, not cosmetic.** Developmental annotations are claims
   with confidence and sources — not editorial labels.
5. **No tradition's worldview is privileged.** All theological, historical, and cosmological
   assertions are captured as tradition-relative claims.
6. **Motifs are first-class entities.** The Thompson Motif Index and ATU are reference systems
   imported as a vocabulary, not as ground truth.
7. **The "lives" tradition has its own epistemics.** Hagiographic and doxographic sources carry
   explicit confidence ceilings reflecting their distance from primary evidence.
8. **Absence and critique belong inside the ontology.** Atheism, secularism, anti-clericalism,
   and non-belief are entities, not the absence of entities.
9. **Narratives and texts are distinct.** A narrative is a story-structure that can exist across
   many texts, oral versions, and retellings. A text is a document with manuscript history.
10. **Symbols are semiotic entities, not mere material objects.** A symbol's power lies in what
    it *means* across traditions, not only in its physical form.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  DOMAIN MODULES                                                       │
│  Religion & Mythology · Philosophy & Sage-Lives · Art & Culture ·    │
│  Polity & Society · Technology · …                                    │
├─────────────────────────────────────────────────────────────────────┤
│  CROSS-CUTTING LAYERS (apply to every entity in every module)         │
│   Claim · Comparative · Developmental · Temporal · Spatial · Media · │
│   Motif · Biographical/Hagiographic · RAG                            │
├─────────────────────────────────────────────────────────────────────┤
│  UNIVERSAL CORE                                                       │
│   Entity · Relationship · Claim · Source · DevelopmentalAnnotation · │
│   TemporalAnchor · SpatialAnchor · MotifEntry · TaleType             │
├─────────────────────────────────────────────────────────────────────┤
│  FEDERATION                                                           │
│   Canonical IDs (KID) · sameAs reconciliation · source provenance ·  │
│   ingestion pipeline (Mythographica · Sacred-Lineage · Kosmotheon ·  │
│   time-thread)                                                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Entity Type Catalogue

This section is the single authoritative listing of all entity types. §4 maps them to modules.
Types are organized by the six ontological layers — the fundamental *kinds* of thing in the
graph, which prevent category confusion (a bodhisattva treated simultaneously as a person, a
concept, and a text).

---

### Layer 0 — Tradition Structure

The organizational skeleton of a religion or intellectual tradition. Contains groupings; not
members or content.

| Entity Type | Definition & Examples |
|---|---|
| **Religion / Tradition** | A broad, persistent tradition with a distinct identity. Buddhism, Christianity, Islam, Hinduism, Confucianism, Taoism. |
| **Branch** | A major doctrinal or historical schism. Theravāda, Mahāyāna; Catholicism, Protestantism; Sunni, Shia. |
| **School / Sect** | A distinctive interpretive or philosophical system within a branch. Mādhyamaka, Yogācāra; Thomism, Calvinism; Hanafi, Shafi'i. |
| **Lineage** | A continuous teacher-disciple transmission chain. Sōtō (from Dōgen), Gelug (from Tsongkhapa), apostolic succession lines. |
| **Community / Institution** | An actual religious or intellectual institution. Sōji-ji monastery, Nalanda university, Vienna Circle. |
| **Movement** | A loosely bounded reform or renewal current. Bhakti movement, charismatic movement, Reformation. |
| **Syncretic Complex** | A blending of multiple traditions functioning as a discrete entity. Santería, Caodaism, Theosophy. |
| **Philosophical School** | An organized intellectual tradition without necessarily religious character. Stoicism, Neoplatonism, Frankfurt School. |
| **Worldview / Stance** | A held position on ultimate questions, including non-belief. Atheism, agnosticism, secular humanism, deism. |
| **Critical Movement** | An organized stance of opposition or critique. Anti-clericalism, secularization, laïcité, freethought. |

*Hierarchy semantics (all are claim-backed when contested):*
- `has_branch` → doctrinal/historical divergence from parent
- `has_school` → interpretive framework within a branch
- `has_lineage` → transmission of authority/practice through persons
- `has_community` → institutional instantiation of a lineage or school

---

### Layer 1 — Agents

Everything that acts, teaches, is venerated, or is interacted with.

**Human agents**

| Subtype | Examples |
|---|---|
| Founder | Siddhārtha Gautama, Jesus of Nazareth, Muḥammad, Laozi (attributed) |
| Teacher / Theologian | Nāgārjuna, Thomas Aquinas, al-Ghazālī, Maimonides |
| Philosopher / Sage | Socrates, Confucius, Plotinus, Ramana Maharshi, Wittgenstein |
| Saint / Mystic | St. Francis, Rabi'a al-'Adawiyya, Meister Eckhart, Mirabai |
| Reformer / Heretic | Martin Luther, Shinran, al-Ḥallāj (by some traditions), Giordano Bruno |
| Monastic | bhikkhu, monk, nun, sādhu, friar, dervish |
| Layperson | upāsaka, parishioner, householder |
| Scientist-Philosopher | Aristotle, Descartes, Newton, Darwin, Einstein |

**Supernatural agents**

| Subtype | Examples |
|---|---|
| Deity | Viṣṇu, Yahweh, Zeus, Amaterasu, Tlāloc |
| Bodhisattva / Buddha | Avalokiteśvara, Amitābha, Maitreya, Tara |
| Saint in glory | Virgin Mary (as intercessor), al-Khiḍr |
| Spirit / Deva / Kami | yakṣa, angel, jinn, kami, loa |
| Demiurge / Trickster | Māra, Satan, Coyote, Loki, Eshu |
| Ancestor entity | pitṛ, venerated lineage founder, ancestral spirit |
| Demon / Asura | rākṣasa, fallen angel, afarit, Ahrimān |
| Mythological figure | Hero, culture hero, cosmic being, primordial giant |

**Collective agents**

| Subtype | Examples |
|---|---|
| Saṅgha / Church-as-body | bhikkhu-saṅgha, the Body of Christ |
| Council / Synod | Buddhist councils (Saṅgīti), Council of Nicaea, Vatican II |
| Personification | Prajñāpāramitā as deity, Sophia (Wisdom), Ma'at |

---

### Layer 2 — Expressions

How a tradition or thinker manifests in the world. This layer is subdivided into four distinct
sub-types: **Texts**, **Narratives**, **Symbols**, **Practices**, and **Material culture**.
Texts and Narratives are explicitly separated — a key architectural decision.

#### 2a. Texts

A text is a *document* — it has a manuscript history, scribal variants, a language, and a
physical or digital instantiation.

| Subtype | Examples |
|---|---|
| Canonical scripture | Tripiṭaka, Bible, Qur'ān, Vedas, Guru Granth Sahib |
| Philosophical treatise | Aristotle's *Metaphysics*, Kant's *Critique of Pure Reason* |
| Commentary | Aṭṭhakathā, Summa Theologiae, Tafsīr, Averroes on Aristotle |
| Liturgical text | Book of Common Prayer, Pūjā manuals, Siddur |
| Hagiography | Jātaka tales, Lives of Saints, *Bhaktamāla* |
| Doxography | Diogenes Laertius, *tabaqāt* biographical dictionaries |
| Philosophical biography | Porphyry's *Life of Plotinus*, Iamblichus's *Life of Pythagoras* |
| Aphorism collection | *Analects*, Nietzsche's aphorisms, Pre-Socratic fragments |
| Letter / correspondence | Epicurus's letters, Seneca's *Epistulae Morales* |
| Hymn / liturgical poem | Rig Veda hymns, Psalms, Sufi qasīda |

> **Oral tradition** is *not* a text subtype. Oral traditions are a distinct source class with
> fundamentally different epistemics and transmission — see §9.3.

#### 2b. Narratives

A narrative is a *story-structure* — a plot, character set, and sequence of events that can exist
simultaneously across multiple texts, oral versions, dramatic retellings, and iconographic programs.
Motifs attach to narratives, not to texts.

```
Narrative {
  id                  : KID
  title               : string            // canonical scholarly title
  summary             : string
  narrative_genre     : cosmogony | theogony | hero_cycle | trickster_tale |
                        wisdom_literature | apocalypse | katabasis | initiation |
                        romance | lament | creation_ex_nihilo | flood | other
  primary_texts       : KID[]             // Text entities that contain this narrative
  oral_variants       : KID[]             // Oral tradition entities
  traditions_carrying : KID[]             // Tradition entities where this narrative lives
  motifs_present      : KID[]             // MotifEntry entities (instantiates_motif)
  tale_types          : KID[]             // TaleType entities (exemplifies_tale_type)
  key_figures         : KID[]             // Agents who appear in the narrative
  developmental       : DevelopmentalAnnotation[]
  claims              : Claim[]
}
```

Examples: The Flood Narrative (exists in Genesis, Gilgamesh, Māhābhārata, Popol Vuh, and 200+
other texts) · The Trojan War · Inanna's Descent · The Garden of Eden · The Buddha's
Enlightenment (as narrative vs. as historical event).

#### 2c. Symbols

A symbol is a *semiotic entity* — a sign whose significance lies in what it consistently evokes
across contexts and traditions. The serpent appears in Genesis, the Caduceus, Kundalini, Quetzalcoatl,
and the Uroboros: not as equivalent concepts, but as a shared semiotic object differently inflected.

```
Symbol {
  id                : KID
  canonical_name    : string           // e.g. "Serpent", "Cross", "Lotus", "Tree"
  visual_description: string           // what it looks like iconographically
  primary_register  : natural | geometric | animal | human | composite | cosmic

  // What it means and does — via relationships
  // symbolizes       → Concept         (what idea the symbol carries)
  // instantiated_in  → Narrative / Text / Practice / Place
  // reinterpreted_as → Symbol (another tradition's symbol this one absorbs)
  // shares_symbolic_grammar_with → Symbol

  attestations      : KID[]            // Traditions / Texts where attested
  developmental     : DevelopmentalAnnotation[]
  claims            : Claim[]
}
```

`shares_symbolic_grammar_with` captures structural kinship between symbols that are not
equivalent but share a deep semiotic logic (serpent + transformation + liminal energy across
dozens of unrelated traditions).

`reinterpreted_as` captures when a tradition takes another tradition's symbol and assigns it
new or inverted meaning (the pre-Christian serpent of wisdom becomes the Christian serpent of
temptation; the Roman cross of execution becomes the Christian symbol of redemption).

#### 2d. Practices & Rituals

| Subtype | Examples |
|---|---|
| Meditation / contemplation | zazen, hesychasm, dhikr, vipassanā |
| Sacrament / rite | Eucharist, baptism, abhiṣeka, bar mitzvah |
| Pilgrimage | Hajj, Kumbha Melā, Camino de Santiago |
| Festival / holiday | Vesāk, Easter, Dīvālī, Ramaḍān, Yom Kippur |
| Asceticism | fasting, celibacy, self-mortification, tapas |
| Ethical observance | Five Precepts, Ten Commandments, Halal dietary laws |
| Divination / oracle | I Ching consultation, Delphic oracle, tarot, Ifa |
| Initiation | Mystery religion initiations, shamanic initiation, confirmation |

#### 2e. Material Culture

| Subtype | Examples |
|---|---|
| Ritual object | Vajra, rosary, Torah scroll, chalice, prayer wheel |
| Sacred architecture | Temple, church, mosque, stūpa, synagogue, kiva |
| Iconography program | Mudra systems, attribute iconography, mandala |
| Music / chant | Gregorian chant, qawwālī, bhajan, kirtan, Vedic chanting |

---

### Layer 3 — Ideas & Concepts

The conceptual content that traditions and thinkers articulate. An idea is the intellectual object
that texts *express* and figures *develop*. It is not a text.

#### Core concept types

| Subtype | Examples |
|---|---|
| Doctrine | Trinity, anātman, tawḥīd, karma, Original Sin |
| Philosophical concept | śūnyatā, substance, wu-wei, logos, qualia, intentionality |
| Ethical principle | ahiṃsā, agape, zakat, golden rule, categorical imperative |
| Soteriological goal | nirvāṇa, mokṣa, salvation, theosis, enlightenment |
| Cosmological model | Buddhist 31 realms, Kabbalistic worlds, Hindu lokas, Norse 9 worlds |
| Eschatological idea | Messianic age, yawm al-qiyāma, mappō, Ragnarök |
| Experience state | samādhi, satori, fanāʾ, henosis, mystical union, ego dissolution |
| Philosophical argument | Ontological argument, Cogito, trolley problem |
| Thought experiment | Plato's Cave, Veil of Ignorance, Zhuangzi's butterfly dream |
| Philosophical problem | Mind-body problem, problem of universals, problem of evil |
| Theory / position | Functionalism, panpsychism, compatibilism, moral realism |
| Term / terminus technicus | Atman, karma, logos, tao, ruach, pneuma, bodhicitta |
| Scholarly theory | Propp's morphology, Campbell's monomyth, Girard's mimetic theory |

#### ConceptInterpretation — the keystone cross-traditional entity

A `ConceptInterpretation` represents one tradition's specific reading of a shared concept node.
It is what prevents "karma" from being forced into a single definition and instead represents
the Theravāda reading, the Mahāyāna reading, the Hindu reading, and the New Age reading as
distinct entities that all relate to the same parent concept.

```
ConceptInterpretation {
  id                : KID
  parent_concept_id : KID              // the shared concept (e.g., "karma")
  tradition_id      : KID              // the tradition making this interpretation
  school_id         : KID?             // optionally more specific (e.g., Theravāda within Buddhism)

  interpretation    : string           // the tradition's specific meaning, in its own terms
  key_terms         : { lang: string, term: string, transliteration: string }[]
  primary_texts     : KID[]            // texts where this interpretation is expressed

  // How this interpretation relates to others
  // contradicts     → ConceptInterpretation (from another tradition)
  // elaborates      → ConceptInterpretation (a refinement of a parent interpretation)
  // reinterprets    → ConceptInterpretation (takes another tradition's reading and transforms it)

  soteriological_role : string?        // what role does this concept play in liberation/salvation?
  developmental       : DevelopmentalAnnotation[]
  claims              : Claim[]
}
```

**Example — "Non-self / Ātman" concept fan:**

```
Concept: Non-self / Ātman (shared node)
  ├─ ConceptInterpretation: Theravāda anattā
  │     tradition: Theravāda Buddhism
  │     interpretation: "No permanent, unchanging self exists in any of the five aggregates"
  │     contradicts → ConceptInterpretation: Advaita Ātman-as-Brahman
  │
  ├─ ConceptInterpretation: Advaita Ātman
  │     tradition: Advaita Vedanta
  │     interpretation: "Ātman is identical with Brahman — pure awareness without object"
  │     contradicts → ConceptInterpretation: Theravāda anattā
  │
  ├─ ConceptInterpretation: Madhyamaka anātman
  │     tradition: Madhyamaka Buddhism
  │     interpretation: "No intrinsic existence in self or dharmas — śūnyatā applies universally"
  │     elaborates → ConceptInterpretation: Theravāda anattā
  │
  └─ ConceptInterpretation: Sāṃkhya Puruṣa
        tradition: Sāṃkhya
        interpretation: "Pure consciousness (Puruṣa) is distinct from matter (Prakṛti) — unchanging but not Brahman"
```

---

### Layer 4 — Space, Time & Events

#### Places

| Subtype | Examples |
|---|---|
| Sacred site — natural | Mount Sinai, River Ganges, Mount Fuji, Glastonbury Tor |
| Sacred site — built | Bodh Gaya temple, Ka'ba, Western Wall, Parthenon |
| Monastery / ashram / academy | Eihei-ji, Plato's Academy, Nalanda, House of Wisdom |
| Region | Magadha, Judea, Tibet, Ionia, Mesopotamia, Gandhāra |
| Mythic / cosmological place | Mount Meru, Valhalla, Duat, Olympus, Mictlan, Pure Land |

#### Time

| Subtype | Examples |
|---|---|
| Historical period / era | Axial Age, Late Antiquity, Islamic Golden Age, Reformation |
| Sacred time — recurring | Sabbath, Ramaḍān, Vassa, Advent, solstice |
| World age / cosmic cycle | Yugas, kalpas, the five suns (Aztec), Hesiodic ages |
| Calendar system | Hebrew, Islamic, Hindu, Buddhist, Julian, Gregorian |

#### Events

| Subtype | Examples |
|---|---|
| Historical event | Council of Nicaea, Hijra, Arab conquests, Reformation |
| Philosophical death-scene | Socrates's death (*Phaedo*), Plotinus's final words, Parinirvāna |
| Genealogy record | Divine genealogies, prophetic lineages, dynastic-religious claims |

#### TransmissionEvent — first-class entity

In Buddhist dharma transmission, Sufi *ijāza*, apostolic ordination, and Tantric initiatory
lineages, the *moment* of transmission is a historically significant event — not reducible to a
bare `teacher_of` edge. It has a date, a place, a ceremony type, a witness set, and often a
contested status.

```
TransmissionEvent {
  id                  : KID
  subtype             : dharma_transmission | ijaza | apostolic_ordination |
                        initiatory_transmission | philosophical_succession | other

  transmitter_id      : KID            // the teacher / initiator
  receiver_id         : KID            // the student / initiate
  lineage_id          : KID?           // which lineage this event belongs to
  tradition_id        : KID

  date_range          : DateRange?
  place_id            : KID?
  witnesses           : KID[]
  ceremony_text       : KID?           // the text used or transmitted (e.g., the dharma)

  // Contested status — often the central question in lineage disputes
  is_contested        : boolean
  dispute_notes       : string?

  // What was transmitted
  transmission_content: string         // e.g., "Rinzai dharma seal", "Sufi silsila"

  claims              : Claim[]
  sources             : KID[]
}
```

**Example — Dōgen's transmission from Rujing:**

```
TransmissionEvent {
  subtype: dharma_transmission
  transmitter: Tiantong Rujing
  receiver: Dōgen Zenji
  lineage: Sōtō (Caodong)
  date_range: { start: 1225, circa: false }
  place: Qingyuan (China)
  is_contested: true   // some scholars dispute the transmission's canonical status
  transmission_content: "shikantaza ('just sitting') as the complete expression of Buddha-dharma"
  claims: [
    Claim { asserted_by: Sōtō tradition, confidence: 0.85, methodology: textual },
    Claim { asserted_by: rival scholars, is_disputed: true, confidence: 0.45 }
  ]
}
```

---

### Layer 5 — Claims

Epistemically neutral statements that traditions or scholars make. Never asserted as true by
the ontology. See §6 for the full claim model.

| Claim type | Example |
|---|---|
| Theological | "God is triune" (Trinitarian Christianity) |
| Historical | "Jesus rose from the dead"; "The Buddha walked at birth" |
| Moral | "Eating beef is prohibited" (many Hindu traditions) |
| Cosmological | "The universe passes through kalpas" |
| Hagiographic | "Pythagoras could be in two places simultaneously" (Iamblichus) |
| Comparative | "Nirvāṇa is functionally equivalent to Mokṣa" (scholarly claim) |
| Developmental | "The Homeric epics primarily express mythic-stage consciousness" |
| Doxographic | "Socrates held that virtue is knowledge" (via Plato and Xenophon) |
| Attribution | "The *Corpus Areopagiticum* was authored by Paul's convert Dionysius" (contested) |

---

## 4. Module Ownership Map

Each entity type is owned by one primary module. Cross-module entities carry `module` tags for
both. Ownership determines which module spec governs the type's extended fields.

| Entity type | Primary module | Cross-module |
|---|---|---|
| Religion / Tradition, Branch, School, Lineage, Community | Religion & Mythology | — |
| Philosophical School, Intellectual Circle, Academy | Philosophy & Sage-Lives | — |
| Worldview / Stance, Critical Movement | Religion & Mythology | Philosophy & Sage-Lives |
| Historical Figure, Saint/Sage, Monastic | Religion & Mythology | Philosophy & Sage-Lives |
| Philosopher, Sage/Wise Person, Scientist-Philosopher | Philosophy & Sage-Lives | Religion & Mythology |
| Deity, Supernatural Being, Mythological Figure | Religion & Mythology | — |
| Text / Scripture, Commentary, Hagiography, Doxography | Religion & Mythology | Philosophy & Sage-Lives |
| Philosophical Treatise, Dialogue, Letter | Philosophy & Sage-Lives | — |
| Narrative | Religion & Mythology | Art & Culture |
| Symbol | Religion & Mythology | Art & Culture |
| Practice / Ritual, Festival, Pilgrimage | Religion & Mythology | — |
| Concept, Doctrine, Experience State | Religion & Mythology | Philosophy & Sage-Lives |
| ConceptInterpretation | Religion & Mythology | Philosophy & Sage-Lives |
| Philosophical Argument, Thought Experiment | Philosophy & Sage-Lives | — |
| MotifEntry, TaleType, NarrativeFunction | Religion & Mythology | Art & Culture |
| ScholarlyNarrativeTheory | Philosophy & Sage-Lives | Religion & Mythology |
| Place (all subtypes) | Core | All modules |
| Historical Period / Era | Core | All modules |
| TransmissionEvent | Religion & Mythology | Philosophy & Sage-Lives |
| Historical Event, Philosophical Death-Scene | Core | All modules |

---

## 5. Relationship Taxonomy

All relationships are grouped into nine families. Every relationship is directional with a
defined domain, range, and inverse. Every relationship is claim-backed when contestable.

**Note on Family J:** The former Family J (Philosophical) has been dissolved. Its four predicates
are absorbed as follows: `founded_school_of` → Family A; `member_of_school` → Family F;
`authored` → Family C; `experience_state_reported` → Family F.

---

### Family A — Tradition Hierarchy

| Predicate | Domain → Range | Meaning | Inverse |
|---|---|---|---|
| `has_branch` | Religion → Branch | Major schismatic division | `branch_of` |
| `has_school` | Branch → School | Interpretive/doctrinal school | `school_of` |
| `has_lineage` | School → Lineage | Chain of transmission | `lineage_of` |
| `has_community` | Lineage → Community | Institutional instantiation | `community_of` |
| `has_subtradition` | Any → Any | Generic sub-grouping | `subtradition_of` |
| `has_subschool` | School → School | Sub-school specialization | `subschool_of` |
| `has_sublineage` | Lineage → Lineage | Lineage branch | `sublineage_of` |
| `founded_school_of` | Person → School/Lineage | The person founded this school or lineage | `founded_by` |
| `syncretizes` | Syncretic Complex → Tradition | Incorporates another tradition's elements | — |
| `opposes` | Tradition/Movement → Tradition/Movement | Institutional or political antagonism | `opposed_by` |

> `opposes` is distinct from `contradicts` (Family D). `contradicts` is logical incompatibility
> between ideas. `opposes` is organized antagonism between institutions or movements:
> the Inquisition opposing heresy; Advaita opposing Mīmāṃsā on liberation; Sunni orthodoxy
> opposing Mu'tazilism.

---

### Family B — Transmission & Influence

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `founded_by` | Tradition/School → Person | Creator/founder |
| `reformed_by` | Tradition/School → Person | Major reformer |
| `transmitted_through` | Tradition → Lineage/Person | Key transmission link |
| `influenced_by` | Any → Any | Historical/cultural influence (asymmetric) |
| `derived_from` | Text/Idea → Text/Idea | Direct genetic relationship |
| `preceded_by` | Entity → Entity | Temporal precedence |
| `anticipated` | Person/Work → Concept | Earlier formulation, often unacknowledged |
| `rehabilitated` | Person → Person/School | Revived and championed after neglect |
| `reinterprets` | Tradition/Person/Work → Concept/Text/Tradition | Takes another's concept or text and assigns new or transformed meaning |

> `reinterprets` is the relationship the whole history of religious and philosophical dialogue
> runs on. Christianity `reinterprets` the Hebrew Bible as prophecy; Islam `reinterprets` both
> as earlier corrupted revelations; Philo `reinterprets` the Torah through Platonic allegory;
> the Renaissance `reinterprets` Plato through Neoplatonism. It is distinct from `commentary_on`
> (textual exegesis) and from `influenced_by` (generic influence). It specifically captures the
> act of appropriating and transforming meaning across tradition boundaries. It always takes
> a `tradition_id` qualifier (who is doing the reinterpreting) and is always a Claim.

---

### Family C — Textual Relations

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `canonical_in` | Text → Tradition | Scripture accepted as authoritative |
| `commentary_on` | Text → Text | Exegetical relationship |
| `recension_of` | Text → Text | Textual variant |
| `translates` | Text → Text | Translation |
| `contains` | Text → Text/Section | Structural inclusion |
| `quotes` | Text → Text | Direct citation |
| `records_views_of` | Doxography → Person | Reports on this person's views |
| `compiled_by` | Text → Person | Compiler of secondary reports |
| `attributed_to` | Text → Person | Uncertain authorship (always a Claim; see §6.3) |
| `authored` | Person → Work | Secure authorship |
| `lost_text_of` | Fragment → Work | Fragment from a lost original |
| `expresses` | Text → Narrative | This text is one instantiation of the narrative |

---

### Family D — Conceptual Relations

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `doctrine_of` | Concept → Tradition | The concept is an official teaching |
| `expressed_in` | Concept → Text | The concept is articulated in that text |
| `contradicts` | Concept/Theory → Concept/Theory | Logical incompatibility |
| `presupposes` | Concept → Concept | Logical dependence |
| `elaborates` | Concept → Concept | More specific formulation of a broader idea |
| `translates_concept` | Person/Work → Concept | Renders an idea across traditions |
| `coined` | Person → Concept/Term | First use of a term in this sense |
| `developed` | Person/School → Concept | Substantive elaboration |
| `refuted` | Person/Work → Argument | Argued against and (claimed to) defeat |
| `synthesized` | Person/Work → Concept + Concept | Brought two ideas together |
| `applies_to` | Theory → Domain | A theory applied to a new domain |
| `symbolizes` | Symbol → Concept | The symbol carries or evokes this concept |
| `embodies` | Agent → Concept | An agent (deity/sage/figure) personifies a concept |

> `embodies` fills the gap between `expressed_in` (concept → text) and `doctrine_of`
> (concept → tradition). Avalokiteśvara *embodies* karuṇā; Christ *embodies* the Logos;
> Saraswati *embodies* vidyā. The relationship goes from Agent to Concept (the agent is the
> living instantiation of the idea, not merely a vehicle for expressing it).

---

### Family E — Cross-Traditional (Comparative)

| Predicate | Domain → Range | Meaning | Who makes it |
|---|---|---|---|
| `equivalent_in` | Any → Any | Functionally or structurally equivalent in a specified respect | Scholarly meta-claim |
| `identified_with` | Any → Any | A tradition explicitly equates two entities | Tradition-internal claim |
| `analogous_to` | Any → Any | Similar structure, different tradition context | Navigational heuristic |
| `borrows_from` | Any → Any | Informal cross-tradition borrowing | Scholarly claim |
| `transforms_into` | Motif → Motif | Lévi-Straussian structural transformation | Scholarly claim |
| `shares_symbolic_grammar_with` | Symbol → Symbol | Structural semiotic kinship without equivalence | Scholarly claim |

#### `equivalent_in` requires a `respect` qualifier

Nirvāṇa and Mokṣa are equivalent in *soteriological function* (liberation from rebirth) but not
in *metaphysics* (Theravāda Nirvāṇa is not union with Brahman). The relationship must always
carry a `respect` field specifying *in what sense* the equivalence holds:

```
equivalent_in {
  subject    : Nirvāṇa (Buddhism)
  object     : Mokṣa (Hinduism)
  respect    : "soteriological function — liberation from the cycle of rebirth"
  confidence : 0.75
  asserted_by: ["Conze, Edward", "Dasgupta, Surendranath"]
  not_equivalent_in: "metaphysical structure — no Ātman/Brahman union in Theravāda"
}
```

#### The three-predicate comparison key

| Predicate | Who claims it | Meaning | Example |
|---|---|---|---|
| `equivalent_in` | Scholars | Functionally/structurally equivalent in a stated respect | Nirvāṇa `equivalent_in` Mokṣa (soteriological function) |
| `identified_with` | A tradition | The tradition explicitly equates two entities | Mahāyāna: Avalokiteśvara `identified_with` Kannon |
| `analogous_to` | Navigation heuristic | Similar structure, different context | Christian heaven `analogous_to` Pure Land |

---

### Family F — Membership, Role & Lineage

| Predicate | Domain → Range | Meaning | Inverse |
|---|---|---|---|
| `member_of` | Person → Community/School | Formal affiliation | — |
| `member_of_school` | Person → PhilosophicalSchool | Philosophical affiliation | — |
| `monastic_in` | Person → Community/Lineage | Ordained member | — |
| `lay_in` | Person → Community | Non-ordained member | — |
| `venerated_in` | Agent → Tradition | Object of devotion | — |
| `teacher_of` | Person → Person | Pedagogical relationship | `student_of` |
| `student_of` | Person → Person | Discipleship (inverse of teacher_of) | `teacher_of` |
| `patriarch_of` | Person → Lineage | Heads a lineage | — |
| `succeeded_as_head` | Person → Person | Diadochē — succession as school head | — |
| `broke_from` | Person/School → Person/School | Explicit departure and divergence | — |
| `experience_state_reported` | Person → ExperienceState | A reported contemplative or mystical state (always a Claim with methodology and source) | — |

> **`teacher_of` / `student_of` clarification:** These are a single inverse pair. Do not
> create a third predicate `studied_under` — it is a synonym for `student_of` and its
> proliferation creates redundant edges. Use `student_of` canonically. The `TransmissionEvent`
> entity (§3.4) captures the *moment* of formal transmission for lineage-critical relationships.

---

### Family G — Space-Time & Practice

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `located_at` | Event/Community → Place | Physical location |
| `occurs_on` | Ritual/Festival → Date/Calendar | Temporal placement |
| `pilgrimage_site_for` | Place → Tradition | Destination for pilgrimage |
| `practice_of` | Practice → Tradition | The practice belongs to the tradition |
| `ritual_involves` | Ritual → Object/Person/Concept | Components of a ritual |
| `sacred_to` | Place → Tradition/Agent | A place's sacred significance |
| `instantiated_in` | Symbol/Narrative → Place/Text/Practice | Where the symbol or narrative appears |

---

### Family H — Epistemic (Claims)

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `asserted_by` | Claim → Tradition/Person | The tradition or scholar holds this claim |
| `disputed_by` | Claim → Tradition/Person | Another party explicitly denies it |
| `based_on` | Claim → Text/Experience | The grounds for the claim |
| `scriptural_basis` | Claim → Text | Specific scriptural warrant |
| `counter_claim` | Claim → Claim | An opposing claim (bidirectional in practice) |
| `qualifies` | Claim → Claim | Adds a scope condition to another claim without opposing it |

---

### Family I — Motif & Narrative

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `instantiates_motif` | Narrative/Text → MotifEntry | Contains an instance of this motif |
| `exemplifies_tale_type` | Narrative/Text → TaleType | Is an instance of this tale type |
| `has_variant_in` | MotifEntry → Tradition/Text | A culture-specific variant |
| `clusters_with` | MotifEntry → MotifEntry | Motifs that regularly co-occur |
| `refines_motif` | MotifEntry → MotifEntry | More specific sub-motif | 
| `composed_of` | TaleType → MotifEntry | The tale type includes this motif |
| `maps_to_propp` | Narrative → NarrativeFunction | Propp morphological function entity |
| `maps_to_campbell` | Narrative/Motif → NarrativeFunction | Hero's Journey stage entity |

> Both `maps_to_propp` and `maps_to_campbell` point to `NarrativeFunction` entities — not to
> strings. Propp's 31 functions and Campbell's 17 stages are each modeled as `NarrativeFunction`
> entities within the `ScholarlyNarrativeTheory` parent, making them queryable.

---

## 6. The Claim Model

Kosmographica stores claims, not facts. Every contestable assertion is a `Claim` entity.

```
Claim {
  id                : KID
  subject_id        : KID             // any Entity OR another Claim (for meta-claims)
  predicate         : string
  object            : KID | literal

  claim_type        : historical | mythological | doctrinal | hagiographic | doxographic
                    | traditional | archaeological | scholarly | comparative
                    | developmental | symbolic | folk | attribution

  // Confidence — canonical numeric + derived band (keep both in sync)
  confidence        : float           // 0.0–1.0 canonical
  confidence_band   : high            // ≥ 0.80
                    | medium          // 0.55–0.79
                    | low             // 0.30–0.54
                    | speculative     // < 0.30
                    | tradition_specific   // orthogonal: tradition holds it but evidence is absent
                    | contested            // orthogonal: active scholarly dispute

  methodology       : linguistic | textual | functional | iconographic | syncretic
                    | archaeological | developmental | hagiographic | doxographic
                    | comparative | oral

  explanation       : string          // 1–2 sentences, scholarly tone

  // Provenance
  source_ids              : KID[]
  secondary_source_ids    : KID[]
  tradition_id            : KID?
  asserted_by             : string[]

  // Scope
  date_range        : DateRange?
  region            : string[]?
  tradition_context : string?
  respect           : string?         // for equivalent_in claims: in what respect?

  // Dispute
  is_disputed       : boolean
  counter_claim_ids : KID[]
  dispute_notes     : string?

  // Editorial
  citation_required : boolean
  reviewed_by       : string?
  review_date       : date?
  recorded_at       : datetime
}
```

> **`disputed` removed from `claim_type`.** A disputed claim is still historical, doctrinal,
> hagiographic, etc. `is_disputed: boolean` already handles dispute status. Keeping `disputed`
> in `claim_type` was a category error — it conflates the *kind* of claim with the *status* of
> the claim.

### 6.1 Confidence ceilings by source type

| Source type | Methodology flag | Max confidence | Rationale |
|---|---|---|---|
| Author's own autograph text | `textual` | 0.90 | Allows error, misattribution |
| Contemporary primary source | `textual` | 0.85 | Eyewitness bias |
| Near-contemporary primary | `textual` | 0.75 | Within a generation |
| Later scholarly reconstruction | `scholarly` | 0.65 | Interpretive; based on primaries |
| Doxographic report | `doxographic` | 0.60 | Secondary; agenda-shaped |
| Philosophical biography | `doxographic` | 0.65 | Near-contemporary; hagiographic elements |
| Hagiographic biography | `hagiographic` | 0.40 | Tendentious by genre; often centuries later |
| Anecdote tradition | `hagiographic` | 0.35 | Attributed sayings; cultural drift |
| Oral tradition (verified by multiple independent lines) | `oral` | 0.55 | Cross-checked |
| Oral tradition (single line, unverified) | `oral` | 0.30 | Variable fidelity |
| Single late source only | any | 0.25 | Insufficient corroboration |

### 6.2 Meta-claims (claims about claims)

The `subject_id` field accepts any KID — including the KID of another Claim. This enables
meta-claims: claims about the epistemic status, interpretation, or validity of another claim.

**Pattern:**

```
// Primary claim
Claim A {
  id: kid:claim/001
  subject_id: kid:entity/plotinus
  predicate: "reached_mystical_union"
  object: kid:concept/henosis
  claim_type: hagiographic
  confidence: 0.55
  asserted_by: ["Porphyry"]
  methodology: hagiographic
}

// Meta-claim disputing the primary claim's interpretation
Claim B {
  id: kid:claim/002
  subject_id: kid:claim/001          // ← points to Claim A
  predicate: "misrepresents_as"
  object: "ecstatic vision rather than sustained non-dual realization"
  claim_type: scholarly
  confidence: 0.60
  asserted_by: ["Hadot, Pierre"]
  explanation: "Hadot argues Porphyry projects later Neoplatonic categories onto Plotinus's
                own more sober language of intellectual contemplation."
}
```

This pattern is also how competing developmental annotations are handled: Wilber's annotation
of a tradition at "mythic altitude" can itself be disputed by Gebser scholars via a meta-claim
pointing to the DevelopmentalAnnotation KID.

### 6.3 Attribution claims (canonical pattern)

For pseudonymous and composite authors (Dionysius the Areopagite, Homer, the Zohar, the
*Corpus Hermeticum*, the Pastoral Epistles), use the `attribution` claim type with the
following canonical pattern:

```
// The text exists as an entity
Entity: Corpus Areopagiticum {
  id: kid:entity/corpus_areopagiticum
  type: Text
  status: historical
}

// Primary attribution claim (the text's own claim)
Claim {
  claim_type: attribution
  subject_id: kid:entity/corpus_areopagiticum
  predicate: "attributed_to"
  object: kid:entity/dionysius_areopagite   // the convert mentioned in Acts 17:34
  confidence: 0.10                          // near-certain pseudonymity
  asserted_by: ["the text itself"]
  methodology: textual
  is_disputed: true
}

// Counter-attribution (scholarly consensus)
Claim {
  claim_type: attribution
  subject_id: kid:entity/corpus_areopagiticum
  predicate: "likely_authored_by"
  object: "unknown Syrian monk, late 5th–early 6th century"
  confidence: 0.85
  asserted_by: ["Stiglmayr, Josef", "Koch, Hugo", "Rorem, Paul"]
  methodology: linguistic
  explanation: "Linguistic and conceptual dependence on Proclus (d. 485 CE) makes earlier
                authorship impossible."
}
```

---

## 7. The Developmental / Consciousness-Mapping Layer

Every entity can carry one or more `DevelopmentalAnnotation` records. Each annotation is itself
a claim — interpretive, contestable, sourced.

### 7.1 Stage frameworks

Stage frameworks track structures of consciousness — relatively stable, sequential, and
hierarchically inclusive ways of making meaning.

| Framework | Key terms (low → high) |
|---|---|
| **AQAL / Integral Theory** (Wilber) | Archaic · Magic · Mythic · Rational · Pluralistic · Integral · Super-Integral |
| **Spiral Dynamics** (Beck & Cowan / Graves) | Beige · Purple · Red · Blue · Orange · Green · Yellow · Turquoise |
| **Gebser's Structures** | Archaic · Magic · Mythic · Mental · Integral |
| **Fowler's Stages of Faith** | Intuitive-Projective · Mythic-Literal · Synthetic-Conventional · Individuative-Reflective · Conjunctive · Universalizing |
| **Kohlberg's Moral Development** | Pre-conventional · Conventional · Post-conventional |
| **Piaget (cognitive)** | Sensorimotor · Pre-operational · Concrete Operational · Formal Operational |
| **Loevinger / Cook-Greuter** | Impulsive · Self-Protective · Conformist · Expert · Achiever · Pluralist · Strategist · Construct-Aware · Unitive |
| **Kegan's Orders of Mind** | Incorporative · Impulsive · Imperial · Interpersonal · Institutional · Inter-individual |
| **Sufi Nafs / Maqāmāt** (stations) | Ammāra · Lawwāma · Mulhima · Muṭmaʾinna · Rāḍiya · Marḍiyya · Kāmila |

> The Sufi *maqāmāt* (stations) are permanent acquisitions through spiritual effort — the
> Sufi tradition's own stage model. They belong here, in the stage framework table.

### 7.2 State frameworks

State frameworks track modes of consciousness — transient, accessible at any stage, but
interpreted differently depending on stage.

| Framework | States |
|---|---|
| **Wilber–Combs Lattice** | Gross (waking) · Subtle (dreaming) · Causal (deep sleep) · Witness · Non-dual |
| **Tibetan Buddhist** | Waking · Dream · Deep Sleep · Rigpa (recognition) · Bardo states |
| **Mandukya / Advaita** | Jagrat · Svapna · Suṣupti · Turīya · Turīyātīta |
| **Theravāda jhāna** | 4 rūpa-jhānas · 4 arūpa-jhānas · nirodha-samāpatti |
| **Hesychast** | Nepsis (watchfulness) · Theoria (vision) · Theosis (deification) |
| **Sufi Aḥwāl** (states) | Qabḍ · Basṭ · Hayba · Uns · Tawājud · Wajd · Wujūd |
| **Transpersonal / Grof** | Sensory · Recollective-Analytic · Symbolic · Integral (COEX systems) |

> The Sufi *aḥwāl* (states) are transient gifts — they arise and pass without permanent
> acquisition. They belong here, in the state framework table, separate from the *maqāmāt*.
> The split corrects the v0.1 error of grouping both under "states."

### 7.3 Lines of development

Lines are relatively independent developmental streams; a person or tradition can be at
different altitudes on different lines simultaneously.

Cognitive · Moral · Spiritual · Aesthetic · Interpersonal · Psychosexual · Somatic/Kinesthetic ·
Emotional · Narrative/Meaning-making · Linguistic

### 7.4 Quadrants (AQAL)

| Quadrant | Label | Scope |
|---|---|---|
| UL | Interior-Individual | Subjective experience, phenomenology, states of consciousness |
| UR | Exterior-Individual | Behavior, brain states, embodiment, observable action |
| LL | Interior-Collective | Culture, shared meaning, worldviews, intersubjectivity |
| LR | Exterior-Collective | Social systems, institutions, economics, ecology |

### 7.5 Altitude key with genre & practice columns

The `altitude` key is the shared cross-framework ordinal that enables aligned queries across
all frameworks simultaneously. All cross-framework equivalences are **claims** with `asserted_by`
and confidence — not ground truth.

| Altitude | AQAL | Spiral Dynamics | Gebser | Fowler | Cook-Greuter | Typical narrative genres | Typical practices |
|---|---|---|---|---|---|---|---|
| `archaic` | Archaic | Beige | Archaic | Stage 1 | Impulsive | Origin chants, undifferentiated cosmogony | Instinctual, pre-ritual |
| `magic` | Magic | Purple + Red | Magic | Stage 2 | Self-Protective | Animistic myth, totem stories, trickster tales | Shamanism, sympathetic magic, blood ritual, totem rites |
| `mythic` | Mythic | Blue | Mythic | Stage 3 | Conformist | Cosmogony, theogony, heroic epic, sacrificial narrative | Temple sacrifice, mystery initiation, prayer, confession, pilgrimage |
| `rational` | Rational | Orange | Mental | Stage 4 | Expert + Achiever | Philosophical dialogue, wisdom literature, critical commentary | Meditation as technique, ethical philosophy, lectio divina |
| `pluralistic` | Pluralistic | Green | Late Mental | Stage 5 | Pluralist | Comparative religion, personal spiritual memoir, hermeneutic | Interfaith practice, therapeutic spirituality, mindfulness |
| `integral` | Integral | Yellow + Turquoise | Integral | Stage 6 | Strategist + Construct-Aware | Integral synthesis, meta-theory, post-metaphysical commentary | Integral life practice, nondual inquiry, embodied shadow work |
| `super-integral` | Super-Integral | — | — | — | Unitive | Post-conceptual, apophatic, transmission literature | Non-practice / Dzogchen, Self-enquiry, wu wei |

### 7.6 The Wilber–Combs lattice as a query structure

States and stages are orthogonal. A person at any stage can access any state temporarily but
interprets it through their stage's conceptual lens:

| State accessed | At mythic stage | At rational stage | At integral stage |
|---|---|---|---|
| Non-dual / Henosis | Devotional union with personal God; absorption into tribal deity | Metaphysical principle; the Absolute as impersonal ground | Full-spectrum non-dual — includes and transcends all previous interpretations |
| Subtle / Dream-like | Visionary rapture, divine encounter, prophetic vision | Hypnagogic state; imagination as epistemological problem | Witness consciousness; subtle body awareness |
| Causal / Absorption | Dreamless union; void-as-death; dark night | Deep meditative absorption; the "night of the soul" | Causal body awareness; formless presence |

Entities annotated with both a `stage_id` and a `state` are queryable across this lattice.
This is the query that produces results like: "all non-dual state experiences interpreted at
the mythic stage" → yields Meister Eckhart's *Gottheit*, Vedantic *turīya* in the Upanishads,
and early Sufi *fanāʾ* literature in the same result set.

### 7.7 DevelopmentalAnnotation schema

```
DevelopmentalAnnotation {
  id           : KID
  target_id    : KID           // any Entity or Claim (including another DevelopmentalAnnotation)
  framework_id : KID
  stage_id     : KID?          // altitude / structure-stage entity
  altitude     : string?       // shared cross-framework key (see §7.5)
  state        : gross | subtle | causal | witness | nondual | null
  quadrant     : UL | UR | LL | LR | null
  line         : string?       // developmental line

  // All developmental readings are claim-grade
  confidence   : float
  asserted_by  : string[]
  sources      : KID[]
  notes        : string?
}
```

### 7.8 Annotating traditions that reject stage models

Several traditions explicitly deny developmental hierarchy: Zen ("no Buddha outside the mind"),
Advaita ("there is no path, there is nowhere to go"), certain strands of Sufism ("the mystic is
already home"). This is not an obstacle to annotation — it is itself data.

**The canonical two-annotation pattern:**

```
// Annotation 1: Annotate the tradition's PRIMARY CONTENT at the relevant altitude
DevelopmentalAnnotation {
  target_id    : kid:entity/zen_buddhism
  altitude     : "rational"       // Zen's koan system engages rational structures to break them
  framework_id : kid:entity/aqal_wilber
  confidence   : 0.65
  asserted_by  : ["Wilber, Ken", "Ferrer, Jorge"]
  notes        : "Zen's primary expression operates at the rational–integral transition"
}

// Annotation 2: Annotate the TRADITION'S META-REJECTION OF STAGES as itself a developmental move
DevelopmentalAnnotation {
  target_id    : kid:entity/zen_anti_hierarchy_stance
  altitude     : "integral"       // the rejection of stages is characteristic of integral-plus
  framework_id : kid:entity/aqal_wilber
  confidence   : 0.60
  asserted_by  : ["Wilber, Ken"]
  notes        : "The explicit denial of stages is itself a post-conventional, integral-stage
                  hermeneutic. The tradition's content (koans, dharma combat) operates at a
                  different altitude from the tradition's meta-commentary on itself."
  is_disputed  : true
  counter_claim_ids : [kid:claim/zen_scholars_object]
}
```

This stores both the tradition's self-understanding (no stages) and the scholarly developmental
reading (this rejection is itself a stage-specific move), without privileging either. The
`is_disputed` flag and `counter_claim_id` ensure the contested nature is surfaced.

---

## 8. The Motif Index Layer

### 8.1 Motif vs. tale type vs. narrative — the three-level stack

| Level | Entity type | Definition | Example |
|---|---|---|---|
| Element | MotifEntry | Smallest persistent narrative element | A1010 "Inundation of earth"; B11 "Dragon" |
| Plot | TaleType | A recognized whole-plot bundle of motifs | ATU 300 "Dragon Slayer" |
| Story | Narrative | A named story-structure existing across texts and traditions | "The Flood Narrative" (across Genesis, Gilgamesh, Māhābhārata…) |

A Narrative `exemplifies_tale_type` (plot level) and `instantiates_motif` (element level). A
TaleType `composed_of` MotifEntries.

### 8.2 Entity schemas

**MotifEntry**

```
MotifEntry {
  // Core entity fields (id, canonical_name, module, etc.)
  motif_system     : tmi | atu | roud | cross | frenzel | culture_area | local
  motif_code       : string         // e.g. "A1010", "ATU 300", "Roud 9"
  motif_category   : string         // TMI top-level letter
  parent_motif_id  : KID?
  child_motif_ids  : KID[]
  canonical_definition : string     // Thompson / Uther verbatim + citation
  scholarly_notes  : string
  propp_function   : KID?           // NarrativeFunction entity (not a string)
  campbell_stage   : KID?           // NarrativeFunction entity (not a string)
  developmental    : DevelopmentalAnnotation[]
}
```

**TaleType**

```
TaleType {
  atu_number            : string
  aarne_number          : string?
  title                 : string
  summary               : string
  core_motifs           : KID[]
  optional_motifs       : KID[]
  primary_culture_area  : string[]
}
```

### 8.3 TMI category axis and consciousness-mapping relevance

| Category | Code | Primary altitude |
|---|---|---|
| Mythological motifs | A | archaic–magic (creation, cosmogony) |
| Animals | B | magic–mythic (transformation, totem) |
| Taboo | C | mythic (prohibition and consequence) |
| Magic | D | magic–mythic (transformation, power objects) |
| The dead | E | cross-stage (afterlife, resurrection) |
| Marvels | F | cross-stage (other worlds, feats) |
| Ogres | G | mythic (devouring, chaos) |
| Tests | H | mythic (initiation, proof of worthiness) |
| The wise and the foolish | J | rational (wisdom literature) |
| Deceptions | K | cross-stage (trickster logic) |
| Reversal of fortune | L | mythic–rational (humility/pride) |
| Ordaining the future | M | mythic (prophecy, fate) |
| Sex | T | magic–mythic (sacred marriage, fertility) |
| Religion | V | all stages |

### 8.4 Index systems covered

| System | Scope | Coverage strategy |
|---|---|---|
| Thompson Motif Index (TMI) | Universal folk literature | Import as `MotifEntry` vocabulary |
| Aarne–Thompson–Uther (ATU) | International tale types | Import as `TaleType` entities |
| Roud Folk Song Index | English-language folk songs | Import for song tradition entities |
| Cross (1952) | Early Irish literature | Culture-area supplement |
| El-Shamy (1995, 2006) | Arab world + *1001 Nights* | Culture-area supplement |
| Kirtley (1971) | Polynesian narratives | Culture-area supplement |
| Guerreau-Jalabert (1992) | Arthurian French verse | Culture-area supplement |
| Bray (1992) | Lives of early Irish saints | Bridges motif + biography layers |
| Frenzel (1976–) | World literary motifs | Extends beyond folk to canonical literature |
| DUCHAS | Irish Folklore Commission | Direct ATU-coded ingestion |

### 8.5 Priority motif clusters for consciousness mapping

**Initiatory death and rebirth** (TMI E0–E99, D1960, F80) — shamanic initiation (magic),
mystery religions (mythic), Sufi *fanāʾ* (mythic-rational), non-dual integration (integral).

**World-tree / axis mundi** (TMI A652) — cosmological centering; maps to the mythic-rational
transition where spatial cosmology becomes inner topology.

**Trickster** (TMI K0–K999, J1700–J2800) — magic (raw transgression) through pluralistic
(deconstruction of fixed identity).

**Divine marriage / hieros gamos** (TMI T100–T199) — fertility magic through alchemical
coniunctio to non-dual integration.

**Descent to the underworld / katabasis** (TMI F80–F109) — Orpheus, Inanna, Persephone,
Aeneas, Dante. Encounter with shadow at every stage.

**Flood** (TMI A1010) — cosmic destruction and renewal. Archaic/magic through apocalyptic-mythic.

---

## 9. The Biographical / Hagiographic Layer

### 9.1 The "life of a sage" as a data cluster

A philosopher's or sage's life is a navigable cluster of entities and claims — not a biography
record. Example (Plotinus):

```
Plotinus (Person)
  ├─ student_of         → Ammonius Saccas
  ├─ teacher_of         → Porphyry, Amelius
  ├─ founded_school_of  → Neoplatonism            [confidence: 0.70, methodology: scholarly]
  ├─ authored           → Enneads (compiled by Porphyry)
  ├─ coined             → "The One" (in Neoplatonic sense)
  ├─ experience_state_reported → Henosis / mystical union
  │     [confidence: 0.55, methodology: hagiographic, source: Porphyry's Life]
  ├─ embodies           → "The One" as realized presence [tradition: Neoplatonism, confidence: 0.60]
  ├─ developmental_annotation → altitude: integral, state: nondual
  │     [asserted_by: Wilber, Ken; confidence: 0.65]
  ├─ recorded_life_in   → Porphyry's Life of Plotinus [PhilosophicalBiography]
  ├─ attested_in        → Eunapius's Lives of the Sophists [Doxography]
  └─ located_at         → Rome · Alexandria
```

### 9.2 Source type epistemics

| Source type | Methodology flag | Max confidence |
|---|---|---|
| Author's autograph text | `textual` | 0.90 |
| Contemporary biography | `textual` | 0.80 |
| Philosophical biography (near-contemporary) | `doxographic` | 0.65 |
| Doxography (secondary compilation) | `doxographic` | 0.60 |
| Hagiographic biography | `hagiographic` | 0.40 |
| Anecdote tradition | `hagiographic` | 0.35 |
| Oral tradition (multi-line verified) | `oral` | 0.55 |
| Oral tradition (single line, unverified) | `oral` | 0.30 |

### 9.3 Oral tradition as a distinct source class

Oral traditions are not a text subtype. They differ from texts in:
- **Transmission:** living performers, not scribes; variation is constitutive, not error
- **Epistemics:** no manuscript history; dating by comparative or contextual evidence only
- **Variation:** multiple simultaneous "correct" versions are normal; no ur-text to reconstruct
- **Ownership:** often community property under CARE principles; access may be restricted

Oral tradition entities carry `methodology: oral` on all derived claims, a `transmission_type`
field (memorized verbatim | formulaic-improvised | free-prose), and a `community_of_origin` KID.

### 9.4 Key hagiographic / doxographic corpora to ingest

| Corpus | Coverage | Source type |
|---|---|---|
| Diogenes Laertius, *Lives of the Eminent Philosophers* | Greek philosophers | Doxography |
| Porphyry, *Life of Plotinus* | Plotinus | Philosophical biography |
| Iamblichus, *Life of Pythagoras* | Pythagoras | Hagiographic philosophy |
| Plutarch, *Lives* | Greek and Roman figures | Historical biography |
| Eunapius, *Lives of the Sophists* | Neoplatonists | Doxography |
| Islamic *tabaqāt* (Ibn Sa'd, etc.) | Islamic scholars | Doxography |
| *Jingde Chuandeng Lu* (lamp records) | Chan/Zen patriarchs | Hagiographic philosophy |
| *Bhaktamāla* | Hindu bhakti saints | Hagiographic philosophy |
| Pali *Theragāthā / Therīgāthā* | Early Buddhist monastics | Hagiographic / documentary |
| Bray (1992), Lives of Irish Saints | Celtic saints | Hagiographic motifs index |

---

## 10. Comparative Layer

Cross-traditional comparison is a first-class operation. See §5 Family E for the full predicate
set. Worked examples of the three-predicate comparison key:

```
Concept: "Ego dissolution / non-self"
  ├─ anātman (Buddhism)
  │     equivalent_in: fanāʾ (Sufism) [respect: "soteriological function — dissolution of ego-boundary"]
  │     analogous_to: kenosis (Christianity) [navigational heuristic]
  │     analogous_to: jīvanmukti (Hinduism)
  │     preceded_by: katabasis motif cluster (TMI F80–F109)
  └─ all ─instantiates_motif─ TMI D1960 "Magic sleep" / E1 "Resuscitation"

Symbol: "Serpent"
  ├─ shares_symbolic_grammar_with: Caduceus (Greek) / Kundalini (Indic) / Uroboros (Hermetic)
  │     [respect: "liminal energy, transformation, wisdom-danger polarity"]
  ├─ reinterpreted_as: Christian serpent of temptation ← from pre-Christian serpent of wisdom
  └─ instantiated_in: Garden of Eden narrative / Asclepius myth / Nāga tradition

Concept: "World-sustaining sacrifice"
  ├─ Yajña (Vedic) ─identified_with─ Puruṣa (Rig Veda 10.90)  [tradition: Vedic]
  ├─ Crucifixion ─reinterprets─ Yajña                          [tradition: Christianity, asserted_by: Panikkar]
  ├─ Aztec cosmic sacrifice ─analogous_to─ Crucifixion          [contested, confidence: 0.45]
  └─ all ─instantiates_motif─ TMI S260 "Sacrifices"
```

---

## 11. Temporal Layer

```
TemporalAnchor {
  date_range   : { start, end, circa: bool, bce: bool }
  precision    : exact | decade | century | period | mythic | unknown
  period_ids   : KID[]       // HistoricalPeriod entities (PeriodO-aligned)
  calendar     : string?     // source calendar; normalized to proleptic Gregorian ISO
  dating_claims: KID[]       // contested datings as Claims, not a single value
}
```

- Contested dates are **Claims**, not a `circa` bool.
- The canonical chronology is the **time-thread** timeline.
- Bitemporality: `recorded_at` (transaction time) vs. `date_range` (valid time).

Key historical periods as entities:

Axial Age (800–200 BCE) · Classical Antiquity · Late Antiquity · Islamic Golden Age ·
Medieval · Early Modern / Reformation · Enlightenment · Romantic / Idealist · Modern ·
Contemporary

---

## 12. Spatial Layer

```
SpatialAnchor {
  place_id     : KID            // links to Place entity
  geometry     : GeoJSON?
  significance : string         // why this place matters to the entity
  sources      : KID[]
}
```

External identifiers: GeoNames (modern), Pleiades (ancient), Getty TGN.

---

## 13. Controlled Vocabulary & Classification Axes

Classification is polyhierarchical — entities carry multiple facet tags, not a single parent
category.

| Axis | Description | Applies to |
|---|---|---|
| **Tradition / Religion** | Which tradition(s) claim or produce this entity | All |
| **Module** | Which domain module owns it | All |
| **Developmental stage (altitude)** | Altitude annotation — always a claim | All |
| **Developmental state** | State annotation — always a claim | All |
| **Period** | Historical era | All |
| **Geography / Region** | Cultural region of origin or significance | All |
| **Narrative genre** | cosmogony / hero cycle / katabasis / wisdom / etc. | Narratives, texts, motifs |
| **Motif category** | TMI top-level category letter | Motifs, narratives |
| **Source quality** | primary / secondary / hagiographic / oral / archaeological | All |
| **Status** | living / historical / reconstructed / disputed / mythic / symbolic | All |
| **Philosophical domain** | Metaphysics / Ethics / Epistemology / Logic / Mind / etc. | Philosophy entities |
| **Contemplative relationship** | None / Adjacent / Integrated / Constitutive | Philosophers, practices |
| **Oral / written** | oral tradition vs. textual tradition | Expressions |

Absence and critique are inside the vocabulary. Atheism, secularism, disenchantment,
anti-clericalism, and freethought are entity-bearing positions with their own traditions
and figures.

---

## 14. Federation & Entity Resolution

### 14.1 Source systems

| System | Native artifact | Maps to |
|---|---|---|
| **Mythographica** | `{meta,nodes,edges}` JSON | nodes → Entity, edges → Claim/Relationship |
| **Sacred-Lineage** | Prisma/SQLite | Figure → Person, TransmissionRelationship → Relationship + TransmissionEvent |
| **Kosmotheon** | MkDocs markdown | DevelopmentalFramework/Stage extraction + long_description |
| **time-thread** | timeline JSON | events → HistoricalEvent + canonical chronology |

### 14.2 Canonical IDs

- **KID** — `kg:entity/<uuid>`, dereferenceable as `https://kosmographica.org/id/<uuid>`
- External IDs: Wikidata · VIAF · GeoNames · Pleiades · Getty AAT/ULAN · PeriodO · CTS URNs

### 14.3 sameAs reconciliation

```
Reconciliation {
  kid           : KID
  source_system : mythographica | sacred_lineage | kosmotheon | time_thread | manual | …
  source_id     : string
  match_method  : exact | curated | embedding | wikidata_bridge
  confidence    : float
  reviewed_by   : string?
}
```

---

## 15. Navigation Design

### 15.1 Seven entry points

| Entry | Primary user | Example query |
|---|---|---|
| By tradition / religion | General explorer | "I want to explore Buddhism" |
| By concept or idea | Concept-driven researcher | "What is nirvāṇa / what is logos?" |
| By figure / person | Biographical explorer | "Tell me about Nagarjuna / Plotinus" |
| By motif | Comparative mythologist | "Show me all flood myths" |
| By developmental stage | Integral researcher | "What is at the mythic-rational transition?" |
| By experience state | Contemplative researcher | "Show me everything associated with non-dual states" |
| By text / scripture | Textual scholar | "I want to explore the Upanishads" |

> **Experience state** (entry point 6) is new in v0.2. "Show me all practices, traditions,
> figures, and motifs associated with non-dual states or ego-dissolution" is one of the most
> important queries for the consciousness-mapping mission. It cannot be reduced to a concept
> query (states are not just ideas) or a stage query (states are orthogonal to stages). Entry
> from the ExperienceState entity type, fanning out via `experience_state_reported`,
> `practice_of`, `embodies`, and `instantiates_motif` to the full relevant subgraph.

### 15.2 Eight traversal axes

1. **Tradition axis** — broader/narrower within a tradition
2. **Conceptual axis** — follow ideas via presupposes, elaborates, contradicts, ConceptInterpretation fan
3. **Biographical / lineage axis** — teacher → student chains, TransmissionEvent nodes
4. **Comparative axis** — cross-traditional via equivalent_in, identified_with, analogous_to, reinterprets
5. **Temporal axis** — derived_from, preceded_by, historical development through eras
6. **Developmental axis** — same altitude in other traditions, adjacent stages, state × stage lattice
7. **Motif / narrative axis** — instantiated motifs, co-occurring motifs, cross-cultural attestations
8. **Spatial axis** — map view, related places, shared sacred sites

### 15.3 Special views

**Stage Panorama** — all entities at one altitude, filterable by entity type, tradition,
geography, period. Side panel shows cross-framework equivalents. Navigation to adjacent stages
and the stage transition zone.

**Lineage Tree** — teacher-student chain visualization anchored on TransmissionEvent nodes.
Highlights contested transmissions. Cross-tradition parallel lineages on the same timeline.

**Motif Atlas** — geographic and temporal map of motif attestations. Cluster view (co-occurring
motifs). Stage view (how a motif's meaning shifts across altitudes).

**Concept Genealogy** — traces a concept through time and across traditions via derived_from,
anticipated, synthesized, reinterprets, translates_concept. Each node shows altitude annotation.

**Comparative Table** — side-by-side view of ConceptInterpretation entities for one parent
concept across multiple traditions, with developmental annotations.

**Symbol Web** — radial graph of a symbol's attestations, showing shares_symbolic_grammar_with
connections and reinterpreted_as transformations across traditions.

### 15.4 Navigation anti-patterns to avoid

- **Religion directory** — forcing a tradition-first path blocks concept, motif, and state entry
- **Flat list** — listing entities under a tradition without grouping by type, period, or stage
- **Confidence black hole** — displaying claims without confidence bands creates false certainty
- **Stage as label** — showing developmental annotations without the claims and disputes behind them
- **Dead ends** — every entity page must have navigable outgoing edges; orphans flagged editorially
- **Conflating narrative and text** — linking motifs to texts instead of narratives breaks the motif query structure

---

## 16. Implementation Notes

- **Graph database:** RDF/OWL export, dereferenceable KIDs, SPARQL endpoint. Postgres with
  typed relationship tables for operational queries.
- **Confidence is always numeric (0.0–1.0) with a derived band.** Never store only the band.
- **Retrieval:** hybrid vector + sparse + GraphRAG. RAG chunks scoped to entity-page sections
  with full structured metadata as context. ConceptInterpretation entities are separate chunks
  from parent Concept entities.
- **Cultural sovereignty:** CARE principles and TK Labels for indigenous and living traditions.
  Sacred/restricted-content flags with access controls are non-negotiable. Oral tradition
  entities default to restricted unless community consent is documented.
- **AI authoring:** AI proposes entities and claims at confidence < 0.7 pending human review.
  Primary AI tasks: motif annotation (proposing TMI codes for Narrative entities);
  ConceptInterpretation extraction (proposing interpretations from tradition-specific text);
  developmental annotation (proposing altitude for entities from descriptive text).
- **Standards:** CIDOC CRM · IIIF · SKOS · PeriodO · Pleiades · CTS URNs.

---

## 17. Open Questions

Unresolved design decisions. Each should be resolved in `docs/governance/decision-log.md`.

1. **Canonical store.** Extend Mythographica's Postgres or stand up a dedicated Kosmographica
   core DB? Affects whether federation is push or pull.

2. **Module namespacing.** One graph with `module` as a node label, or per-module namespaces?

3. **Altitude key ownership.** Adopt Wilber's altitude color scheme as canonical, or define a
   Kosmographica-neutral scale? The neutral scale avoids integral-theory branding but requires
   re-mapping all existing Kosmotheon content.

4. **Non-Western stage models.** The altitude key is derived primarily from Western integral
   frameworks. We need an advisory process with tradition-informed scholars before annotating
   non-Western traditions' core entities.

5. **Shared concepts across modules.** "Karma" is religious with a philosophical elaboration
   history. "Consciousness" is philosophical with a contemplative elaboration history. Need a
   binding rule for where borderline entities live. *Proposed rule:* entities live in the module
   of their *primary reception context*; cross-module `expressed_in` and `doctrine_of` handle
   the rest. Requires editorial review for all borderline cases before ingestion.

6. **Living philosophers and thinkers.** Do CARE-principle-style protections extend to living
   philosophers and their evolving or unpublished views?

7. **Psychedelic / entheogenic research corpus.** Grof's COEX systems, Johns Hopkins psilocybin
   studies — state-phenomenology data that is neither traditional nor purely philosophical.
   Which module, and what source epistemics?

8. **Propp and Campbell as annotation systems vs. entity hierarchies.** Each function/stage
   should be a `NarrativeFunction` entity (established in v0.2). Resolved in principle; needs
   the full 31 Propp functions and 17 Campbell stages populated as entities in the data.

9. **ConceptInterpretation granularity.** Should every tradition that engages with a concept
   get a ConceptInterpretation entity, or only traditions with a substantially distinct reading?
   A Hindu peasant's understanding of karma and Śankara's reading are both "Hindu" — how fine
   is the grain?

10. **Symbol vs. Concept boundary.** The lotus *symbolizes* purity and enlightenment (Symbol →
    Concept via `symbolizes`). But "purity" is also a Concept with its own interpretations. At
    what point does a symbol become a concept, or vice versa? Need an editorial decision rule.

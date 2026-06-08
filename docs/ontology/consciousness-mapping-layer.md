# Consciousness-Mapping Layer — Design

> **Status:** draft · **Date:** 2026-05-31
> **Upstream:** `docs/ontology/gap-analysis.md` §2.3 · `docs/core-meta-model.md` §4
> **Purpose:** Specify the content (not just the architecture) of the developmental layer —
> what frameworks we include, how cross-framework mapping works, and how the layer enables
> the core mission of tracing human consciousness development across all traditions.

---

## 1. The mission restated precisely

The goal is not to *rank* traditions on a developmental scale. It is to make the following
queries possible:

> "What entities across all modules — deities, texts, philosophers, motifs, practices, concepts —
> have been interpreted as expressing or corresponding to the *initiatory threshold* between the
> mythic and rational stages of consciousness, across multiple independent frameworks?"

> "Show me all contemplative practices annotated as primarily addressing non-dual *states* rather
> than *stages*, across Buddhist, Sufi, Hindu, and Christian traditions."

> "What is the full genealogy of the concept of 'ego death' — from shamanic death-rebirth motifs
> through mystery religions through 20th-century psychedelic research through integral theory?"

These queries require: (1) stage annotation on entities, (2) state annotation on entities,
(3) cross-framework equivalence mapping, (4) temporal traversal of concept genealogy.

---

## 2. The developmental frameworks to include

The core meta-model (§4) names frameworks but does not specify their content. Here we specify
the full set and their relationships.

### 2.1 Stage frameworks (vertical axis — structures of consciousness)

| Framework | Author | Stages (key terms) | Primary domain |
|---|---|---|---|
| **AQAL / Integral Theory** | Ken Wilber | Archaic → Magic → Mythic → Rational → Pluralistic → Integral → Super-Integral | Comprehensive meta-framework |
| **Spiral Dynamics** | Beck & Cowan (from Clare Graves) | Beige → Purple → Red → Blue → Orange → Green → Yellow → Turquoise | Cultural values systems |
| **Gebser's Structures** | Jean Gebser | Archaic → Magic → Mythic → Mental → Integral | Cultural phenomenology |
| **Fowler's Stages of Faith** | James Fowler | Intuitive-Projective → Mythic-Literal → Synthetic-Conventional → Individuative-Reflective → Conjunctive → Universalizing | Religious/faith development |
| **Kohlberg's Moral Development** | Lawrence Kohlberg | Pre-conventional → Conventional → Post-conventional | Moral reasoning |
| **Piaget (cognitive)** | Jean Piaget | Sensorimotor → Pre-operational → Concrete Operational → Formal Operational | Cognitive development |
| **Loevinger / Cook-Greuter** | Jane Loevinger, Susanne Cook-Greuter | Impulsive → Self-Protective → Conformist → Expert → Achiever → Pluralist → Strategist → Construct-Aware → Unitive | Ego development |
| **Kegan's Orders of Mind** | Robert Kegan | Incorporative → Impulsive → Imperial → Interpersonal → Institutional → Inter-individual | Subject-object development |
| **Vervaeke's Relevance Realization** | John Vervaeke | (not strictly a stage model, but maps onto participatory, perspectival, propositional knowing) | Cognitive science of meaning |

### 2.2 State frameworks (horizontal axis — modes of consciousness)

| Framework | Author | States | Primary domain |
|---|---|---|---|
| **Wilber–Combs Lattice** | Wilber + Allan Combs | Gross (waking) / Subtle (dreaming) / Causal (deep sleep) / Witness / Non-dual | Integral theory of states |
| **Tibetan Buddhist states** | Vajrayana tradition | Waking / Dream / Deep sleep / Rigpa (recognition) / Bardo states | Contemplative phenomenology |
| **Yoga Nidra / Mandukya** | Advaita / Yoga tradition | Jagrat / Svapna / Suṣupti / Turīya / Turīyātīta | Hindu phenomenology |
| **Theravāda jhāna states** | Pali tradition | 4 form jhānas + 4 formless jhānas + nirodha | Buddhist meditation |
| **Hesychast states** | Eastern Christian tradition | Nepsis / Theoria / Theosis | Christian mysticism |
| **Sufi maqāmāt and aḥwāl** | Islamic mystical tradition | Stations (permanent acquisitions) vs. States (transient gifts) | Sufi psychology |
| **Psychedelic state phenomenology** | Grof, Masters/Houston, Barrett | Sensory / Recollective-Analytic / Symbolic / Integral | Transpersonal psychology |

### 2.3 Lines of development

Lines are relatively independent streams of development that can be at different stages simultaneously.
The following lines are tracked in Kosmographica:

Cognitive · Moral · Spiritual · Aesthetic · Interpersonal · Psychosexual · Somatic / Kinesthetic ·
Emotional · Narrative / Meaning-making · Linguistic

A `DevelopmentalAnnotation` can specify which line is being annotated, allowing claims like:
"Ibn Arabi operates at an integral stage on the spiritual line but a conventional stage on the
political line" — which is itself a contested scholarly claim with confidence and sources.

### 2.4 Quadrants (AQAL lenses)

| Quadrant | Label | Scope |
|---|---|---|
| Upper-Left (UL) | Interior-Individual | Subjective experience, phenomenology, consciousness states |
| Upper-Right (UR) | Exterior-Individual | Behavior, brain states, embodiment, observable action |
| Lower-Left (LL) | Interior-Collective | Culture, shared meaning, worldviews, intersubjectivity |
| Lower-Right (LR) | Exterior-Collective | Social systems, institutions, economics, ecology |

Motifs, rituals, and practices are often quadrant-specific: a meditation practice has UL
(subjective state), UR (physiological correlate), LL (cultural meaning), and LR (institutional
form) aspects. The `quadrant` field on `DevelopmentalAnnotation` captures which aspect is being
annotated.

---

## 3. Cross-framework altitude mapping

The core meta-model uses a shared `altitude` key to enable cross-framework alignment. Here we
specify the full mapping.

### 3.1 The altitude key values

```
archaic        →  pre-egoic, undifferentiated, fusion with environment
magic          →  egocentric, animistic, power-oriented, pre-causal
mythic         →  ethnocentric, conformist, mythological-literal, group-identity
rational       →  worldcentric, formal-operational, individual achievement, evidence-based
pluralistic    →  relativistic, post-conventional, sensitivity to context and marginalized voices
integral       →  construct-aware, second-tier, integrates previous stages
super-integral →  third-tier, non-symbolic, beyond conceptual frameworks
```

### 3.2 Cross-framework alignment table

| Altitude | Wilber/AQAL | Spiral Dynamics | Gebser | Fowler | Cook-Greuter | Kohlberg |
|---|---|---|---|---|---|---|
| archaic | Archaic | Beige | Archaic | Stage 1 | Impulsive | Pre-conventional 1 |
| magic | Magic | Purple + Red | Magic | Stage 2 | Self-Protective | Pre-conventional 2 |
| mythic | Mythic | Blue | Mythic | Stage 3 | Conformist | Conventional |
| rational | Rational | Orange | Mental | Stage 4 | Expert + Achiever | Post-conventional 1 |
| pluralistic | Pluralistic | Green | Late Mental | Stage 5 | Pluralist | Post-conventional 2 |
| integral | Integral | Yellow + Turquoise | Integral | Stage 6 | Strategist + Construct-Aware | — |
| super-integral | Super-Integral | — | — | — | Unitive | — |

**Important:** All cross-framework equivalences in this table are themselves `Claim` entities with
`confidence` and `asserted_by`. Wilber's stage-color mappings are contested; Gebser scholars
dispute the alignment with Spiral Dynamics. The table is a useful navigational heuristic, not
a ground truth.

### 3.3 Implementation in the data model

The `DevelopmentalStage` entity's `equivalents` field (array of KIDs to stages in other
frameworks) is populated from this table as claims with `confidence: 0.7` and
`asserted_by: ["Wilber, Ken", "Beck, Don", "Kosmographica editorial"]`. Where scholars dispute
an alignment, a counter-claim is added.

---

## 4. The Wilber–Combs lattice as a query structure

The key insight of the Wilber–Combs lattice is that states and stages are orthogonal: a person
at any stage can temporarily access any state, but they will *interpret* that state through the
lens of their stage. This generates distinct experiential and doctrinal profiles for the same
state at different stages.

This is extraordinarily useful for comparative religion:
- A **mystical union experience** (non-dual state) interpreted at the **mythic stage** produces
  devotional theism (union with God as person)
- The same experience interpreted at the **rational stage** produces philosophical mysticism
  (union as metaphysical principle)
- At the **pluralistic stage**: psychologized mysticism (the experience is real but culturally
  constructed)
- At the **integral stage**: full-spectrum embrace (the experience is real, its stage-specific
  interpretations are all partial but valid)

Entities annotated with both a `stage_id` and a `state` field on their `DevelopmentalAnnotation`
can be queried on this lattice. A user can ask: "Show me all entities that represent a non-dual
state interpreted at the mythic stage" — and get Meister Eckhart's *Godhead*, the Vedantic *nirguna
Brahman* as described in the Upanishads, and the Buddhist *tathāgatagarbha* doctrine all in
one result set.

---

## 5. Phenomenological and contemplative frameworks

A gap in most integral frameworks is the detailed phenomenology of contemplative states.
These frameworks need inclusion as `DevelopmentalFramework` entities:

**Edmund Husserl's phenomenology** — intentionality, epoché, reduction, intersubjectivity.
The philosophical toolkit for describing first-person experience without reductionism.

**Francisco Varela's neurophenomenology** — bridges Husserlian phenomenology with cognitive
science; the framework for grounding contemplative state claims in empirical research.

**Tibetan Bardo Thodol phenomenology** — the most detailed traditional map of state transitions
in death and dream. Structured in three bardos (dying, dharmata, becoming), each with distinct
phenomenological signatures.

**The Cloud of Unknowing tradition** — apophatic phenomenology of contemplative states in
Christian mysticism.

**Sufi psychology (nafs model)** — the seven stations of the soul (ammāra, lawwāma, mulhima,
muṭmaʾinna, rāḍiya, marḍiyya, kāmila). A stage-state hybrid model.

Each of these becomes a `DevelopmentalFramework` entity with its stages/states/axes specified
as `DevelopmentalStage` entities, and cross-mapped to the altitude key via claims.

---

## 6. The consciousness genealogy query

One of the highest-value use cases: tracing a concept's development through time and across
stages. Example: **the concept of ego-dissolution**.

```
Query: "Show me the genealogy of ego-dissolution as a concept and experience"

Results (traversal):
  MotifEntry: TMI E600 "Reincarnation" + E481 "Land of the dead"
    → attested in shamanic traditions (altitude: archaic-magic)
  MotifEntry: D1960 "Magical sleep" + F80 "Journey to other world"
    → Mystery religions (altitude: mythic)
  Concept: kenosis (Christian self-emptying) 
    → Paul of Tarsus, Meister Eckhart (altitude: mythic-rational)
  Concept: fanāʾ (Sufi annihilation)
    → Al-Hallaj, Ibn Arabi (altitude: mythic-rational-pluralistic)
  Concept: anātman (Buddhist non-self)
    → Pali canon, Nagarjuna, Chan (altitude: rational-integral)
  Concept: ego death
    → Stanislav Grof, psychedelic research (altitude: pluralistic)
  Concept: witness consciousness / non-dual awareness
    → Ramana Maharshi, Wilber (altitude: integral)
  Theory: neurophenomenology of self-dissolution
    → Varela, Thompson, Metzinger (altitude: rational-pluralistic)
```

This traversal is possible only if: (1) all these entities exist in the graph, (2) they are
connected via relationship chains (motif → concept → person → work), and (3) they all carry
developmental annotations with the altitude key.

---

## 7. What this layer is NOT

- **Not a ranking of traditions.** Annotating a tradition's texts at "mythic altitude" is not a
  judgment that the tradition is primitive — it is a description of a structural feature of its
  primary mode of expression. Traditions contain material at every altitude simultaneously.
- **Not a single truth.** Every developmental annotation is a claim with `asserted_by` and
  confidence. The system stores *multiple competing annotations* from different scholars.
- **Not complete.** Most entities will begin without developmental annotations. The layer is
  populated incrementally by editors and AI assistants, with human review required.

---

## 8. Open questions

1. **Altitude for non-Western frameworks.** The altitude key is derived primarily from Wilber's
   integral framework, which has been criticized for mapping non-Western traditions onto a
   Western developmental schema. We need an advisory process involving scholars from each
   tradition before assigning altitude annotations to their core entities.

2. **How to handle frameworks that reject stage models.** Zen, Advaita, and certain strands of
   Sufism explicitly deny developmental stages ("there is no path, there is nowhere to go"). Do
   we annotate them at "integral" (which is itself a stage — a meta-irony), or create a special
   flag for "post-stage"? Wilber's answer is "integral and above"; Krishnamurti scholars would
   object. This is an open editorial question.

3. **The psychedelic and entheogenic research corpus.** Stanislav Grof's COEX systems, the
   Johns Hopkins psilocybin studies, the MAPS MDMA research — these generate state-phenomenology
   data that belongs in the consciousness-mapping layer but is not traditional in origin. Where
   does this fit in the module structure?

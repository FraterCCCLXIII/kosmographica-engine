# Philosophy & Sage-Lives Module — Ontology Design

> **Status:** draft · **Date:** 2026-05-31
> **Upstream:** `docs/ontology/gap-analysis.md` §2.2, §2.5
> **Downstream:** `docs/modules/philosophy-science.md` (to be written)
> **Conforms to:** `docs/core-meta-model.md`

---

## 1. Scope

This module covers:
- **Philosophers and sages** — historical thinkers across all traditions, from pre-Socratic Greeks
  to contemporary philosophers, from Upanishadic rishis to Chan patriarchs, from Islamic mutakallimūn
  to African ubuntu philosophers
- **Philosophical schools and movements** — not traditions in the religious sense, but organized
  intellectual lineages: the Academy, the Stoa, the Neoplatonists, the Vienna Circle, the Kyoto School
- **Philosophical works** — texts, arguments, aphorisms, dialogues, treatises
- **Philosophical concepts** — ideas that circulate primarily in philosophical (rather than
  devotional or mythological) contexts, though these blur at the edges
- **The lives of philosophers** — the biographical and hagiographic record of thinkers' lives,
  encounters, deaths, and reported sayings, as a distinct source class with its own epistemics

**Boundary with the Religion & Mythology module:** The two modules overlap significantly. Plotinus
is a philosopher and a mystic. Nagarjuna is a philosopher and a Bodhisattva. Al-Ghazali is a
theologian and a philosopher. The rule: entities live in the module that best describes their
*primary context of reception*. Cross-module relationships are first-class. A person can have
`member_of` relationships to entities in both modules.

---

## 2. Entity types

### 2.1 Persons

| Entity Type | Definition | Examples |
|---|---|---|
| **Philosopher** | A thinker whose primary activity is philosophical argumentation and concept-formation | Plato, Nagarjuna, Ibn Rushd, Kant, Wittgenstein |
| **Sage / Wise Person** | A figure venerated primarily for wisdom, often with a biographical mythologization | Socrates, Confucius, Laozi, Diogenes of Sinope, Ramana Maharshi |
| **Theologian-Philosopher** | Figure who works at the intersection of theological tradition and philosophical reasoning | Aquinas, al-Ghazali, Maimonides, Shankara, Dōgen |
| **Scientist-Philosopher** | Figure whose philosophical significance derives from or accompanies scientific work | Aristotle, Descartes, Newton, Darwin, Einstein |
| **Contemplative-Philosopher** | Figure whose philosophy is inseparable from contemplative practice | Plotinus, Meister Eckhart, Nāgārjuna, Ibn Arabi |

All are subtypes of the core `Person` entity type; the subtype controls which relationship
vocabulary and page sections are available.

### 2.2 Intellectual lineages and communities

| Entity Type | Definition | Examples |
|---|---|---|
| **Philosophical School** | An organized intellectual tradition with a founding figure, doctrines, and succession | Platonism, Stoicism, Advaita Vedanta, Kyoto School |
| **Philosophical Movement** | A looser intellectual current without tight institutional succession | German Idealism, Pragmatism, Phenomenology, Poststructuralism |
| **Academy / Institution** | A physical institution of philosophical teaching | Plato's Academy, Nalanda, House of Wisdom, École Normale |
| **Intellectual Circle** | An informal group with shared orientation | Vienna Circle, Frankfurt School, Bloomsbury Group |

### 2.3 Works and texts

| Entity Type | Definition | Examples |
|---|---|---|
| **Philosophical Treatise** | A sustained single-author argument | Aristotle's *Metaphysics*, Kant's *Critique*, Husserl's *Ideas I* |
| **Dialogue** | A philosophical work in dialogue form | Plato's dialogues, Hume's *Dialogues Concerning Natural Religion* |
| **Commentary** | A work whose primary purpose is explaining another text | Proclus on Plato, Averroes on Aristotle, Vasubandhu on the Abhidharma |
| **Aphorism Collection** | A work organized as discrete sayings | Pre-Socratic fragments, *Analects*, Nietzsche's *Twilight of the Idols* |
| **Letter / Correspondence** | Philosophical content transmitted in epistolary form | Epicurus's letters, Seneca's *Epistulae*, Leibniz–Clarke correspondence |
| **Lecture Notes / Doxography** | Secondary records of a philosopher's teaching | Reports of Socrates, Epictetus's *Discourses* (by Arrian), the doxographic tradition |

### 2.4 Arguments and concepts

| Entity Type | Definition | Examples |
|---|---|---|
| **Philosophical Argument** | A named, reconstructable argument that circulates in the literature | Ontological argument, Cogito, Trolley problem, Ship of Theseus |
| **Philosophical Concept** | An idea whose primary home is philosophical discourse | Substance, essence, qualia, aporia, logos, śūnyatā (in its Madhyamaka context) |
| **Thought Experiment** | A hypothetical scenario used to probe philosophical intuitions | Descartes's evil demon, Plato's cave, Rawls's veil of ignorance, Schrödinger's cat |
| **Philosophical Problem** | A named open question | Mind-body problem, problem of universals, problem of evil, hard problem of consciousness |
| **Theory / Position** | A named philosophical stance | Functionalism, panpsychism, compatibilism, moral realism |

### 2.5 Source types — the "lives" tradition

This is the gap identified in the gap analysis. The biographical-doxographic tradition requires
its own entity type and epistemics.

| Entity Type | Definition | Examples |
|---|---|---|
| **Doxography** | A secondary compilation of philosophers' views and lives | Diogenes Laertius, Theophrastus, Stobaeus, the Arabic *tabaqāt* |
| **Philosophical Biography** | A sustained biographical treatment of a single figure | Porphyry's *Life of Plotinus*, Iamblichus's *Life of Pythagoras* |
| **Hagiographic Philosophy** | A biographical text that mythologizes the philosopher's life | Lives of the Zen Patriarchs (*Jingde Chuandeng Lu*), Lives of the Neoplatonists |
| **Anecdote Tradition** | A corpus of attributed sayings and anecdotes circulating around a figure | The *chreia* tradition (Cynic/Stoic), Confucian anecdotes, Sufi *maqāmāt* |

**Epistemics of this source class.** Claims derived from doxographic or hagiographic sources
receive a distinct methodology flag: `methodology: hagiographic` or `methodology: doxographic`.
This affects confidence ceilings:
- A claim about Pythagoras's views derived solely from Iamblichus (written ~800 years later) cannot
  exceed `confidence: 0.4`
- A claim about Plato's views derived from his own dialogues can reach `confidence: 0.85`
- A claim about Socrates's views is always `methodology: doxographic` and capped at `0.65`
  (because everything comes through Plato, Xenophon, and Aristophanes)

---

## 3. Relationship vocabulary

### 3.1 Intellectual lineage relationships

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `studied_under` | Person → Person | Direct teacher-student relationship |
| `founded_school_of` | Person → PhilosophicalSchool | Founder relationship |
| `member_of_school` | Person → PhilosophicalSchool | Affiliation |
| `succeeded_as_head` | Person → Person (within school) | Diadochē — succession as head of a school |
| `broke_from` | Person/School → Person/School | Explicit departure and divergence |
| `rehabilitated` | Person → Person/School | Revived and championed after neglect |

### 3.2 Conceptual relationships

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `coined` | Person → Concept/Term | First use of a term in this sense |
| `developed` | Person/School → Concept/Theory | Substantive elaboration |
| `refuted` | Person/Work → Argument/Theory | Argued against and (claimed to) defeat |
| `anticipated` | Person/Work → Concept/Theory | Earlier formulation, often unacknowledged |
| `synthesized` | Person/Work → Concept + Concept | Brought two traditions/ideas together |
| `applied_to` | Theory → Domain | A philosophical theory applied to a new domain |
| `presupposes` | Concept → Concept | Logical dependence |
| `contradicts` | Theory → Theory | Logical incompatibility |
| `translates` | Person/Work → Concept (across traditions) | Renders an idea from one tradition into another's vocabulary |

### 3.3 Textual relationships

| Predicate | Domain → Range | Meaning |
|---|---|---|
| `authored` | Person → Work | Standard authorship |
| `attributed_to` | Work → Person | Uncertain authorship (a claim, not a fact) |
| `compiled_by` | Doxography → Person | The compiler of secondary reports |
| `records_views_of` | Doxography → Person | Reports on this philosopher's views |
| `translated_by` | Work → Person (translator) | Translation relationship |
| `lost_text_of` | Fragment → Work | Fragment from a lost original |

---

## 4. The "life of a sage" as a data cluster

A philosopher's life in Kosmographica is not a biography record — it is a navigable cluster of
entities and claims. The pattern:

```
Plotinus (Person)
  ├─ studied_under → Ammonius Saccas (Person)
  ├─ taught → Porphyry, Amelius (Persons)
  ├─ founded → Neoplatonism (PhilosophicalSchool) — claim, confidence 0.7
  ├─ authored → Enneads (Work, compiled by Porphyry)
  │    └─ contains → "On the Good or the One" (Ennead VI.9)
  ├─ coined → The One (Concept, in Neoplatonic sense)
  ├─ experience_state_reported → Henosis / mystical union (ExperienceState) — claim, methodology: hagiographic
  ├─ developmental_annotation → stage: integral, state: nondual (asserted_by: Wilber, Ken)
  ├─ source_of_life → Porphyry's *Life of Plotinus* (PhilosophicalBiography)
  ├─ attested_in → Eunapius's *Lives of the Sophists* (Doxography)
  └─ located_at → Rome (Place) + Alexandria (Place)
```

The "life" is the sum of these relationships and their associated claims. A dedicated UI view
assembles them into a narrative page — but the underlying data is fully graph-traversable.

### 4.1 The death-scene as a structured event

Philosophical death-scenes are a recurring literary topos and often carry doctrinal weight
(Socrates's *Phaedo*, the death of Plotinus as reported by Porphyry, the Parinirvāna of the
Buddha). They deserve a distinct entity type:

```
death_scene {
  entity_type   : HistoricalEvent (subtype: PhilosophicalDeathScene)
  subject_id    : KID              // the philosopher
  reported_in   : KID[]            // source texts
  last_words    : string?          // if attested; tagged as Claim
  witnesses     : KID[]            // persons present
  doctrinal_significance : string  // why traditions remember it
  confidence    : float            // based on source quality
}
```

---

## 5. Classification axes

| Axis | Values | Notes |
|---|---|---|
| **Tradition affiliation** | Western, Indic, Chinese, Islamic, African, Indigenous, ... | Polyhierarchical — Averroes spans Islamic and Western |
| **Period** | Pre-Socratic, Hellenistic, Late Antique, Medieval, Early Modern, Modern, Contemporary | Cross-culture periods need care — use time-thread eras |
| **Domain of inquiry** | Metaphysics, Epistemology, Ethics, Logic, Aesthetics, Philosophy of Mind, Political Philosophy, Philosophy of Religion | Facet tag; a thinker can have multiple |
| **Methodology** | Analytic, Continental, Phenomenological, Dialectical, Apophatic, Dialogical | |
| **Developmental stage** | Inherited from core §4 — applies to both the thinker and their primary framework | A claim, not a fact |
| **Relationship to contemplative practice** | None / Adjacent / Integrated / Constitutive | How central practice is to their philosophy |

---

## 6. Consciousness-mapping relevance

The philosophy module is essential to the consciousness-mapping mission because philosophers and
sages are the *articulators* of developmental stages. The pattern:

- **Mythic stage:** The pre-Socratics, early Upanishadic rishis, Confucius — figures who work at
  the transition from mythological to rational thinking
- **Rational stage:** Classical Greek philosophy, Scholasticism, early Islamic philosophy —
  systematic rational frameworks
- **Pluralistic stage:** Hermeneutics, pragmatism, phenomenology — frameworks that relativize
  the rational stance
- **Integral stage:** Wilber, Aurobindo, Gebser, Whitehead — frameworks that attempt to include
  all previous stages

The `developmental_annotation` on philosopher entities makes this traversable. A user can ask:
"Show me all philosophers whose primary framework is annotated at the rational–pluralistic
transition" — and get Nietzsche, William James, Husserl, and Nāgārjuna in the same result set.

---

## 7. Open questions

1. **Shared concepts between religion and philosophy modules.** "Karma" is a religious concept
   with a philosophical elaboration history. "Consciousness" is a philosophical concept with
   religious/contemplative elaboration. The rule — entities live in one module, cross-module
   `expressed_in` and `related_to` relationships do the rest — but we need explicit guidance on
   borderline cases.

2. **Pseudonymous and composite authors.** "Dionysius the Areopagite" is almost certainly not the
   person the texts claim; "Homer" may be multiple people; the *Zohar* is attributed to Shimon bar
   Yochai but likely written by Moses de León. These need an `attribution_claim` pattern, not just
   `attributed_to`.

3. **Living philosophers.** The CARE principles and sovereignty concerns primarily address
   indigenous and living religious communities. Do they extend to living philosophers? We need a
   policy for including/excluding living thinkers and their unpublished or evolving views.

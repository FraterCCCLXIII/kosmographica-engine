# Cosmograph Catalog — Design

> **Status:** draft · **Date:** 2026-06-07
> **Upstream:** `docs/ontology/gap-analysis.md` · `docs/ontology/consciousness-mapping-layer.md` · `docs/core-meta-model.md`
> **Purpose:** Catalog humanity's sustained attempt to map reality itself — not as a flat list of
> "cosmologies," but as a documented history of **cosmographs**: structured maps of cosmos, psyche,
> and their fusion across cultures and periods.

---

## 1. Framing

For a project such as Kosmographica, the subject should not be conceived as a mere list of
cosmologies. It is better understood as a **history of humanity's sustained attempt to map reality
itself**.

These maps group into three broad families:

| Family | Domain |
|---|---|
| **Topological Cosmographs** | Physical reality — earth, heavens, universe |
| **Metaphysical Cosmographs** | Being, spirit, gods, afterlife, emanation, salvation |
| **Psychological Cosmographs** | Mind, consciousness, soul, cognition, development |

One of the most striking features of pre-modern thought is that these three categories were typically
**fused**: a medieval *mappa mundi* was at once a diagram of geography, a statement about the order
of creation, and a chart of the soul's journey. Kosmographica records both the modern analytic split
and the historical fusion via multi-domain tagging on each cosmograph entity.

---

## 2. Master catalog (structured records)

Canonical seed data for **`Cosmograph`** entities. Each row is one map; columns align with the
per-cosmograph metadata schema (§4). The **Type** column is the primary meta-taxonomy class; **Domain**
and **Topology** are facets. Ingestion should emit one entity per row with `data` fields populated
from these columns and `source_system: manual` until a dedicated adapter exists.

> **Count:** 74 cosmographs · spans prehistory through agentic AI (2025+).
> Machine-readable copy: [`data/cosmographs/catalog.csv`](../../data/cosmographs/catalog.csv).

| Cosmograph | Tradition | Region | Dates | Type | Domain | Topology | Human Position | Liberation Path | Primary Sources |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Three Worlds | Paleolithic Shamanism | Eurasia | 50,000 BCE+ | Metaphysical | Cosmos | Vertical Layers | Mediator | Shamanic ascent | Ethnographic reconstruction |
| World Tree | Proto-Indo-European | Eurasia | Prehistoric | Metaphysical | Cosmos | Tree | Midpoint | Axis ascent | Comparative mythology |
| Megalithic Sky Map | Neolithic Europe | Europe | 3500 BCE | Topological | Cosmos | Astronomical | Observer | Alignment | Stonehenge, Newgrange |
| Sumerian Cosmos | Sumerian | Mesopotamia | 3500 BCE | Metaphysical | Cosmos | Layered | Servant of gods | Divine order | ETCSL, Enuma Elish |
| Babylonian World Map | Babylonian | Mesopotamia | 600 BCE | Topological | Earth | Circular Disk | City-centered | None | BM 92687 |
| Egyptian Cosmos | Egyptian | Nile Valley | 3000 BCE | Metaphysical | Cosmos | Layered Geography | Participant in Ma'at | Afterlife navigation | Pyramid Texts |
| Duat Map | Egyptian | Nile Valley | 2000 BCE | Metaphysical | Afterlife | Journey Map | Soul traveler | Solar union | Amduat |
| Zoroastrian Cosmos | Iranian | Persia | 1000 BCE | Metaphysical | Cosmos | Dualistic | Cosmic combatant | Frashokereti | Avesta |
| Vedic Three Worlds | Vedic | India | 1500 BCE | Metaphysical | Cosmos | Triple Realm | Sacrificer | Ritual ascent | Rig Veda |
| Puranic Universe | Hindu | India | 300 BCE+ | Metaphysical | Cosmos | Concentric Rings | Karma-bound soul | Moksha | Bhagavata Purana |
| Jain Lokapurusha | Jain | India | 500 BCE | Metaphysical | Cosmos | Cosmic Person | Jiva | Liberation | Tiloya Pannatti |
| Buddhist Meru Cosmos | Buddhist | India | 300 BCE | Metaphysical | Cosmos | Concentric Realms | Sentient being | Nirvana | Abhidharmakosa |
| Abhidharma Mind Map | Buddhist | India | 300 BCE | Psychological | Mind | Taxonomic Network | Observer | Awakening | Dhammasangani |
| Pañca-Kośa | Upanishadic | India | 700 BCE | Psychological | Consciousness | Nested Layers | Atman | Self-realization | Taittiriya Upanishad |
| Sāṃkhya Tattvas | Hindu | India | 500 BCE | Psychological | Reality | Emanation Tree | Purusha | Discrimination | Sāṃkhya Kārikā |
| Yoga Psychology | Hindu | India | 300 BCE | Psychological | Mind | Developmental | Practitioner | Samadhi | Yoga Sutras |
| Homeric Cosmos | Greek | Greece | 800 BCE | Topological | Cosmos | Flat Disk | Hero | Fate | Iliad |
| Hesiodic Cosmos | Greek | Greece | 700 BCE | Mythic | Cosmos | Genealogical Tree | Mortal | Divine alignment | Theogony |
| Pythagorean Cosmos | Greek | Greece | 600 BCE | Philosophical | Cosmos | Numerical Harmony | Rational knower | Purification | Aristotle |
| Platonic Cosmos | Greek | Greece | 360 BCE | Metaphysical | Being | Hierarchy | Rational soul | Ascent to Forms | Timaeus |
| Aristotelian Cosmos | Greek | Greece | 350 BCE | Scientific | Cosmos | Nested Spheres | Rational animal | Contemplation | De Caelo |
| Stoic Cosmos | Greek-Roman | Mediterranean | 300 BCE | Philosophical | Cosmos | Living Organism | Rational part | Living by Logos | Diogenes Laertius |
| Hermetic Cosmos | Hermetic | Egypt | 100 BCE | Mystical | Soul | Planetary Ascent | Divine spark | Gnosis | Corpus Hermeticum |
| Gnostic Pleroma | Gnostic | Mediterranean | 100 CE | Mystical | Spirit | Emanation Tree | Exiled spark | Return to Fullness | Nag Hammadi |
| Neoplatonic Cosmos | Neoplatonic | Mediterranean | 250 CE | Metaphysical | Being | Emanation | Soul | Henosis | Plotinus |
| Proclean Cosmos | Neoplatonic | Mediterranean | 450 CE | Metaphysical | Being | Hyper-hierarchy | Soul | Reversion | Proclus |
| Merkabah Cosmos | Jewish | Levant | 200 CE | Mystical | Heaven | Palace Ascent | Mystic | Heavenly ascent | Hekhalot |
| Kabbalistic Tree | Jewish | Europe | 1200 CE | Mystical | Being | Graph Tree | Soul | Devekut | Zohar |
| Christian Celestial Hierarchy | Christian | Byzantine | 500 CE | Metaphysical | Heaven | Nine Orders | Human | Union with God | Pseudo-Dionysius |
| Great Chain of Being | Christian | Europe | 500 CE | Metaphysical | Reality | Hierarchy | Midpoint | Sanctification | Aquinas |
| Islamic Falasifa Cosmos | Islamic | Middle East | 900 CE | Metaphysical | Cosmos | Spheres | Rational soul | Intellect | Ibn Sina |
| Illuminationist Cosmos | Islamic | Persia | 1200 CE | Mystical | Being | Light Hierarchy | Soul | Illumination | Suhrawardi |
| Akbarian Cosmos | Sufi | Islamic World | 1200 CE | Mystical | Being | Levels of Being | Perfect Human | Realization | Ibn Arabi |
| Mappa Mundi | Medieval Christian | Europe | 1300 CE | Topological | World | Sacred Geography | Pilgrim | Salvation | Hereford Map |
| Dantean Cosmos | Christian | Italy | 1320 CE | Narrative Cosmograph | Soul | Vertical Journey | Pilgrim | Beatific Vision | Divine Comedy |
| Llullian Cosmos | Christian | Spain | 1300 CE | Logical Cosmograph | Knowledge | Combinatorial Wheels | Knower | Divine understanding | Ars Magna |
| Fludd Cosmos | Rosicrucian | Europe | 1600 CE | Esoteric | Cosmos | Great Chain | Microcosm | Spiritual ascent | Fludd |
| Kircher Cosmos | Jesuit | Europe | 1600 CE | Universal Cosmograph | Knowledge | Hybrid Diagram | Scholar | Knowledge | Kircher |
| Copernican Cosmos | Scientific | Europe | 1543 | Scientific | Cosmos | Heliocentric | Observer | Knowledge | De Revolutionibus |
| Keplerian Cosmos | Scientific | Europe | 1596 | Scientific | Cosmos | Platonic Geometry | Observer | Mathematical insight | Mysterium Cosmographicum |
| Bruno Infinite Cosmos | Philosophical | Europe | 1584 | Metaphysical | Cosmos | Infinite Space | Infinite being | Intellectual liberation | Bruno |
| Newtonian Universe | Scientific | Europe | 1687 | Scientific | Cosmos | Infinite Mechanics | Observer | Knowledge | Principia |
| Linnaean Taxonomy | Scientific | Europe | 1735 | Classification | Life | Tree | Naturalist | Knowledge | Systema Naturae |
| Darwinian Tree | Scientific | Europe | 1859 | Evolutionary | Life | Branching Tree | Species | Adaptation | Origin of Species |
| Theosophical Cosmos | Theosophy | Global | 1888 | Esoteric | Spirit | Layered Planes | Soul | Evolution | Secret Doctrine |
| Anthroposophical Cosmos | Anthroposophy | Europe | 1904 | Esoteric | Spirit | Evolutionary Hierarchy | Ego | Spiritual science | Steiner |
| Freud Topography | Psychology | Europe | 1900 | Psychological | Mind | Layered | Ego | Analysis | Interpretation of Dreams |
| Jungian Psyche | Psychology | Europe | 1915+ | Psychological | Psyche | Mandala | Self | Individuation | CW9 |
| Psychosynthesis | Psychology | Europe | 1920+ | Psychological | Psyche | Developmental | Self | Integration | Assagioli |
| Relativistic Cosmos | Physics | Global | 1915 | Scientific | Universe | Curved Manifold | Observer | Knowledge | Einstein |
| Big Bang Universe | Physics | Global | 1927+ | Scientific | Universe | Expanding Space | Observer | Knowledge | Lemaître |
| Inflationary Universe | Physics | Global | 1981+ | Scientific | Universe | Multiverse | Observer | Knowledge | Guth |
| Cosmic Web | Astrophysics | Global | 2000+ | Scientific | Universe | Network | Observer | Knowledge | SDSS |
| Piaget Development | Psychology | Global | 1952 | Developmental | Mind | Stages | Child | Cognitive growth | Piaget |
| Kohlberg Development | Psychology | Global | 1958 | Developmental | Ethics | Stages | Moral actor | Ethical maturity | Kohlberg |
| Graves Emergent Cycles | Psychology | Global | 1960s | Developmental | Values | Spiral | Person | Evolution | Graves |
| Loevinger Ego Development | Psychology | Global | 1976 | Developmental | Ego | Stages | Self | Development | Loevinger |
| Kegan Orders | Psychology | Global | 1982 | Developmental | Meaning | Stages | Subject-object self | Growth | Kegan |
| Spiral Dynamics | Integral | Global | 1996 | Developmental | Culture | Spiral | Participant | Evolution | Beck |
| AQAL | Integral | Global | 1995 | Integral | Reality | Multi-axis Matrix | Holon | Integral realization | Wilber |
| General Systems Theory | Systems | Global | 1968 | Systems | Reality | Network | System node | Adaptation | Bertalanffy |
| Cybernetics | Systems | Global | 1948 | Systems | Control | Feedback Loops | Agent | Regulation | Wiener |
| Autopoiesis | Systems | Global | 1972 | Systems | Life | Self-producing Network | Organism | Viability | Maturana |
| Gaia Theory | Systems | Global | 1979 | Ecological | Earth | Living Planet | Earth participant | Sustainability | Lovelock |
| Luhmann Social Systems | Sociology | Global | 1984 | Systems | Society | Communication Network | Observer | Understanding | Luhmann |
| Network Science | Complexity | Global | 2000+ | Information | Reality | Graph | Node | Understanding | Barabási |
| Information Cosmology | Physics | Global | 1989+ | Information | Reality | Information Structure | Observer | Knowledge | Wheeler |
| Integrated Information Theory | Consciousness | Global | 2004+ | Psychological | Consciousness | Information Geometry | Experiencer | Integration | Tononi |
| Semantic Web | Information | Global | 2001+ | Information | Knowledge | Graph | User | Knowledge | Berners-Lee |
| Wikidata | Information | Global | 2012+ | Knowledge | Knowledge | Graph | Contributor | Knowledge | Wikidata |
| OpenAlex | Information | Global | 2022+ | Knowledge | Science | Citation Graph | Researcher | Knowledge | OpenAlex |
| Embedding Space Cosmology | AI | Global | 2013+ | Cognitive | Meaning | Vector Space | Query point | Inference | word2vec |
| Foundation Model World Models | AI | Global | 2020+ | Cognitive | Reality | Latent Space | Agent | Prediction | Transformers |
| Agentic Cosmology | AI | Global | 2025+ | Cognitive | Knowledge | Dynamic Graph | Agent | Coordination | Multi-agent systems |

### 2.1 Cross-links to other ontology layers

| Catalog cluster | Related doc |
|---|---|
| Developmental rows (Piaget → AQAL) | `consciousness-mapping-layer.md` §2 |
| Psychological / consciousness rows | `consciousness-mapping-layer.md` §2.2 |
| Mythic / shamanic / religious rows | `religion-mythology.md` · `Cosmology` entity type |
| Philosophical rows | `philosophy-sage-lives-module.md` |
| Wikidata · OpenAlex · Agentic | Kosmographica as instance (§1 framing) |

---

## 3. Kosmographica meta-taxonomy

The master catalog uses **Type** as the primary classification axis. Values in use (74 entries):

| Type | Count (approx.) | Maps to analytic family (§1) |
|---|---|---|
| Metaphysical | 18 | Metaphysical |
| Scientific | 10 | Topological |
| Psychological | 7 | Psychological |
| Mystical | 7 | Metaphysical + Psychological |
| Developmental | 7 | Psychological |
| Systems | 5 | Psychological / Information |
| Topological | 4 | Topological |
| Philosophical | 3 | Metaphysical |
| Information | 3 | Information |
| Knowledge | 2 | Information |
| Cognitive | 3 | Psychological / AI |
| Mythic | 1 | Metaphysical |
| Narrative Cosmograph | 1 | Fused |
| Logical Cosmograph | 1 | Psychological |
| Esoteric | 2 | Metaphysical |
| Universal Cosmograph | 1 | Fused |
| Classification | 1 | Topological |
| Evolutionary | 1 | Topological |
| Integral | 2 | Psychological |
| Ecological | 1 | Systems |
| Sociology | 1 | Systems |
| Complexity | 1 | Information |
| Consciousness | 1 | Psychological |

Broader browse groupings (navigation facet — coarser than Type):

1. Shamanic & Mythic · 2. Philosophical & Scientific · 3. Religious & Mystical · 4. Psychological &
   Developmental · 5. Systems & Ecological · 6. Information & Knowledge · 7. AI & Cognitive

Each catalog row is a first-class **`Cosmograph`** entity. **Type**, **Domain**, and **Topology** are
orthogonal facets; the three analytic families (§1) are derived tags for cross-module queries.

---

## 4. Per-cosmograph metadata schema

Core fields populated from the master catalog (§2); additional fields via claims and relationships.

| Field | Catalog column | Description |
|---|---|---|
| `label` | Cosmograph | Display name |
| `tradition` | Tradition | Religious, philosophical, or cultural school |
| `region` | Region | Geographic anchor |
| `date_range` | Dates | Composition / attestation span |
| `cosmograph_type` | Type | Primary meta-taxonomy class (§3) |
| `domain` | Domain | Cosmos, mind, soul, knowledge, universe, etc. |
| `topology` | Topology | Structural form of the map |
| `human_position` | Human Position | Where the person sits in the map |
| `liberation_path` | Liberation Path | Traversal, salvation, or growth model |
| `primary_sources` | Primary Sources | Canonical texts, artefacts, or corpora |

Extended fields (not in seed CSV — added via curation):

| Field | Description |
|---|---|
| **Number of levels** | Counted strata, realms, or stages |
| **Axis mundi** | Present / absent; form if present |
| **Afterlife structure** | Realms, judgments, cycles |
| **Consciousness model** | Layers, states, faculties mapped |
| **Historical influences** | `influenced_by` relationships |
| **Descendants** | `adapted_by` relationships |

Contestable mappings (e.g. "Dante's cosmos is primarily psychological vs. theological") are
**claims** with confidence, sources, and dispute tracking per `docs/core-meta-model.md` — not
editorial assertions in entity `data` alone.

---

## 5. Graph relationships (vocabulary sketch)

Proposed module relationships (to register in `docs/governance/controlled-vocabulary.md`):

| Predicate | Meaning |
|---|---|
| `influenced_by` | Prior cosmograph shaped this map |
| `adapted_by` | Later cosmograph derives from this one |
| `maps_same_domain_as` | Scholarly comparison link across cultures |
| `instantiates_topology` | Entity uses a named topology pattern |
| `fuses` | Explicit fusion of topological + metaphysical + psychological layers |
| `corresponds_to_developmental_framework` | Link to `DevelopmentalAnnotation` target |

---

## 6. Downstream integration

| Decision here | Flows to |
|---|---|
| `Cosmograph` entity type + metadata schema | `docs/modules/philosophy-science.md` (and religion-mythology extension for mythic/shamanic maps) |
| Meta-taxonomy facets | `docs/governance/controlled-vocabulary.md` |
| Relationship predicates | Module vocabulary + ingestion adapters |
| Navigation / browse entry | `docs/ontology/navigation-design.md` · `docs/frontend/app-architecture.md` |
| Developmental cross-links | `docs/ontology/consciousness-mapping-layer.md` |

With this structure, Kosmographica becomes not merely a catalogue of cosmologies, but a **documented
history of humanity's evolving maps of reality itself**.

**WORLD RELIGION & MYTHOLOGY**

**KOSMOGRAPHICA — RELIGION & MYTHOLOGY DOMAIN MODULE**

Specification & Implementation Document

Version 1.2  ·  Architecture, Data Model, Navigation, Comparative Layer, Developmental Layer & RAG Design

| Designed for: Human browsing · AI training & RAG retrieval · Graph-based relationship mapping · Cultural heritage archiving · Comparative religion scholarship |
| --- |

> **Module conformance.** This document specifies the **Religion & Mythology domain module** of
> Kosmographica — the first and best-developed module of a larger system whose mission is a total
> record of human thought, culture, and development through an integral developmental lens. It
> **conforms to** the [Kosmographica Core Meta-Model](../core-meta-model.md):
> the base entity schema below is a *profile* of the core `Entity`; the claim model is the core
> `Claim` model; the comparative layer is unchanged; and the **integral/developmental layer**
> (core §4) is layered on top — see §17.
>
> Where this document and the core meta-model differ, **the core meta-model governs** (notably:
> claims use a canonical numeric `confidence` 0.0–1.0 with a derived band — see §15 and §11.2).

# 1. Vision & Core Principles

This document specifies the architecture, data model, navigation design, and implementation plan for
the Religion & Mythology module of Kosmographica — a comprehensive civilizational knowledge graph
covering world religions, mythologies, spiritual traditions, sacred texts, figures, deities,
practices, and their relationships across all of human history. As a Kosmographica module it shares
the universal core, the federation layer, and the cross-cutting claim, comparative, developmental,
temporal, and media layers with the system's other domains (Philosophy & Science, Art & Culture,
Polity & Society, Technology).

## 1.1 Design Philosophy

| FOUNDATIONAL PRINCIPLE |
| --- |
| Do not make "religions" the only top-level unit. Make everything an entity with typed relationships. |
| The system is a graph-first encyclopedia + RAG corpus + media archive — not a religion directory. |
| No entity "owns" a concept. Reincarnation, karma, enlightenment, and sacrifice are nodes in a civilizational semantic graph that traditions relate to differently, not properties of a single religion. |

## 1.2 The Three Failure Modes to Avoid

| Failure Mode | Why It Breaks |
| --- | --- |
| Religion-centric hierarchy | Forces syncretic, cross-cultural, and contested concepts into artificial ownership |
| Fact without provenance | Flattens myth, doctrine, lineage memory, and academic history into false certainty |
| Entity without claim layer | AI cannot distinguish "tradition asserts X" from "scholarship demonstrates X" |
| Concept without interpretation layer | "Reincarnation" is not one thing — Hindu, Buddhist, Pythagorean, Kabbalistic versions are distinct |
| Symbols and experience states omitted | Loses the embodied, visual, and mystical dimensions of tradition |

## 1.3 Governing Standards

The system aligns with established linked-data and cultural-heritage standards:

- **Wikidata model:** Statements with qualifiers, references, and confidence ranks — the exact pattern needed for disputed religious history
- **SKOS:** Taxonomies, thesauri, and subject-heading structures for controlled vocabularies. The Kosmographica controlled vocabulary is built **fresh**, anchored on the Mythographica tradition/relation taxonomy and its epistemic methodology rules — external glossaries are treated as unverified leads, not load sources (see core meta-model §8)
- **CIDOC CRM:** Cultural-historical data integration for complex entity relationships
- **IIIF:** Interoperable delivery and presentation of cultural heritage images
- **RDF / JSON-LD:** Linked-data export for external scholarly and AI consumption
- **CARE Principles & Traditional Knowledge (TK) Labels:** Data-sovereignty and cultural-sensitivity framework for indigenous and living traditions, with sacred/restricted-content flags and access controls
- **External identifier authorities:** Wikidata, VIAF (persons), GeoNames & Pleiades (places, incl. ancient), Getty AAT/ULAN (art & iconography), PeriodO (historical periods), CTS URNs (classical texts)

# 2. Complete Entity Ontology

The ontology consists of 26 top-level entity types. Every entity is a node; all information is expressed through typed relationships with provenance and confidence metadata.

### Traditions & Communities

| Entity Type | Description / Examples |
| --- | --- |
| Tradition / Religion | World religions, indigenous traditions, mystery schools, philosophical schools |
| Subtradition / School / Sect | Theravāda, Sunni, Reformed, Śaiva Siddhānta, etc. |
| Lineage | Guru-disciple chains, apostolic successions, dharma transmission lines |
| Institution | Vatican, Nalanda, Shaolin, Gelug Order, Ramakrishna Mission |
| Order / Monastery / Ashram | Specific organized communities with physical seat |

### Persons & Beings

| Entity Type | Description / Examples |
| --- | --- |
| Historical Figure | Founders, teachers, prophets, mystics, scholars, reformers |
| Saint / Sage / Guru | Venerated individuals within a tradition |
| Deity / Divine Being | Gods, goddesses, avatars, divine manifestations |
| Supernatural Being | Angels, demons, spirits, bodhisattvas, archons |
| Mythological Figure | Heroes, tricksters, culture heroes, cosmic beings |
| Ancestor Entity | Ancestral spirits, deified ancestors, lineage founders |

### Knowledge & Narrative

| Entity Type | Description / Examples |
| --- | --- |
| Text / Scripture | Canonical scriptures, sutras, tantras, Vedas, Bible, Quran |
| Commentary | Bhāṣya, Talmud, patristic writings, scholastic glosses |
| Oral Tradition | Chant traditions, transmitted narratives, unwritten lineages |
| Myth / Narrative | Creation myths, cosmogonic narratives, hero cycles |
| Mythological Motif | Flood, dying god, cosmic egg, world tree, trickster, divine twins |
| Scholarly Theory | Academic interpretive frameworks, comparative hypothesis |

### Concepts & Cosmology

| Entity Type | Description / Examples |
| --- | --- |
| Concept | Karma, reincarnation, salvation, enlightenment, grace, nonduality |
| Concept Interpretation | Tradition-specific reading of a shared concept |
| Cosmology | Buddhist 31 realms, Kabbalistic worlds, Hindu lokas, Norse 9 worlds |
| Sacred Time / World Age | Yugas, eschatological eras, millennial periods, Mappō |
| Experience State | Samādhi, satori, mystical union, vision quest, revelation, possession |

### Practices & Ritual

| Entity Type | Description / Examples |
| --- | --- |
| Practice / Ritual | Meditation, prayer, sacrifice, initiation, pilgrimage, yoga |
| Holiday / Festival | Diwali, Easter, Ramadan, Vesak, Navaratri, Yom Kippur |
| Calendar System | Hebrew, Islamic, Hindu, Buddhist, Julian, Gregorian |

### Material & Visual Culture

| Entity Type | Description / Examples |
| --- | --- |
| Symbol | Cross, Om, Dharma Wheel, Menorah, Yin-Yang, Ankh, Trident |
| Ritual Object | Vajra, rosary, Torah scroll, chalice, prayer wheel, lingam |
| Art / Iconography | Iconographic programs, mudras, attribute systems, visual canons |
| Image / Artifact Record | Specific digitized images, manuscripts, archaeological objects |

### Space & History

| Entity Type | Description / Examples |
| --- | --- |
| Place — Sacred Site | Mount Sinai, Bodh Gaya, Mecca, Jerusalem, Varanasi, Delphi |
| Place — Built Site | Temples, churches, mosques, stupas, synagogues, monasteries |
| Place — Region | Magadha, Judea, Tibet, Ionia, Mesopotamia, Gandhara |
| Place — Mythic/Cosmological | Mount Meru, Valhalla, Duat, Olympus, Mictlan, Pure Land |
| Historical Event | Council of Nicaea, Arab conquests, Buddhist councils, Reformation |
| Genealogy Record | Divine genealogies, prophetic lineages, dynastic-religious claims |

### Language & Sources

| Entity Type | Description / Examples |
| --- | --- |
| Language | Sanskrit, Pali, Hebrew, Greek, Latin, Avestan, Tibetan, Arabic |
| Term / Terminology Entry | Atman, karma, logos, tao, ruach, pneuma, bodhicitta |
| Claim Record | Explicit provenance-tagged assertions with confidence level |
| Source / Manuscript | Primary sources, inscriptions, archaeological finds, recordings |
| Collection / Archive | Libraries, museum collections, manuscript repositories |

# 3. Core Data Model

> This module's data model is a **profile of the Kosmographica universal core** (core meta-model §2–§3).
> The base entity schema below maps onto the core `Entity`; `relationships`, `claims`, and
> `comparative_edges` are the core cross-cutting layers; and every node also carries a `module`
> (`religion_mythology`), a `source_system`, `external_ids`, and a `developmental` annotation set
> (§17). Confidence is canonically numeric (0.0–1.0) with a derived band — see §15.2.

## 3.1 Universal Entity Schema

Every entity, regardless of type, inherits this base schema. Type-specific fields extend it.

| BASE ENTITY SCHEMA |
| --- |
| entity { |
| id : UUID (canonical) |
| type : EntityType (enum, see §2) |
| subtype : string[] |
| canonical_name : string |
| alternate_names : { name: string, language: string, script: string }[] |
| short_description : string (≤ 280 chars — used in graph labels & RAG summaries) |
| long_description : string (full encyclopedic text) |
| tradition_ids : UUID[] |
| region_ids : UUID[] |
| date_range : { start: date, end: date, circa: bool, BCE: bool } |
| status : living | historical | reconstructed | disputed | mythic | symbolic |
| confidence_level : high | medium | low | traditional_only | speculative |
| source_quality : primary | secondary | tertiary | oral | archaeological |
| relationships : Relationship[] // see §3.2 |
| claims : Claim[] // see §3.4 |
| images : ImageRecord[] // see §6 |
| texts : UUID[] // linked text entities |
| articles : Article[] |
| citations : Citation[] |
| embeddings : vector[] // for RAG retrieval |
| rag_chunks : RAGChunk[] // see §5 |
| language_terms : { lang: string, term: string, transliteration: string }[] |
| wikidata_id : string? |
| geonames_id : string? // for place entities |
| last_reviewed : date |
| editor_notes : string |
| } |

## 3.2 Relationship Types

All relationships are typed, directional, and carry provenance. Relationships themselves can have qualifiers (date, region, confidence, source).

- **Hierarchy & Membership:** part_of  ·  subtradition_of  ·  member_of  ·  founded_by  ·  split_from  ·  merged_into  ·  derived_from
- **Lineage & Transmission:** teacher_of  ·  student_of  ·  lineage_successor_of  ·  initiated_by  ·  ordained_by  ·  dharma_heir_of
- **Intellectual:** influenced_by  ·  commentary_on  ·  responds_to  ·  synthesized_with  ·  equivalent_to  ·  syncretized_with
- **Textual:** attested_in  ·  quoted_in  ·  composed_by  ·  translated_by  ·  canonical_for  ·  apocryphal_for
- **Spatial:** located_in  ·  contains  ·  near  ·  pilgrimage_destination_for  ·  mythic_equivalent_of  ·  symbolically_mapped_onto
- **Temporal:** occurred_during  ·  preceded_by  ·  contemporary_with  ·  destroyed_by  ·  restored_by
- **Conceptual:** related_to  ·  opposed_by  ·  transcended_by  ·  aspect_of  ·  subset_of  ·  universalized_from
- **Narrative:** appears_in  ·  depicts  ·  symbolizes  ·  exemplifies_motif  ·  parallel_to  ·  variant_of
- **Epistemic:** disputed_as  ·  possibly_related_to  ·  claimed_to_be  ·  rejected_by_scholarship  ·  corroborated_by
- **Visual/Material:** depicted_in  ·  iconographic_attribute_of  ·  associated_symbol  ·  ritual_object_of

### Relationship Record Schema

| RELATIONSHIP SCHEMA |
| --- |
| relationship { |
| id : UUID |
| subject_id : UUID |
| predicate : RelationshipType (enum) |
| object_id : UUID |
| qualifiers { |
| date_range : DateRange? |
| region : string? |
| context : string? // e.g. "in Mahāyāna context only" |
| } |
| claim_type : traditional | scholarly | archaeological | mythological | speculative |
| confidence : high | medium | low | disputed |
| sources : Citation[] |
| notes : string |
| } |

## 3.3 Claim-Based Data Layer

**Do not store only facts — store claims.** This is the most critical architectural decision. Without an explicit claim layer, AI systems will conflate tradition, myth, hagiography, and academic history into a single false certainty.

| EXAMPLE: CLAIM RECORD |
| --- |
| subject: Mahavatar Babaji |
| predicate: teacher_of |
| object: Lahiri Mahasaya |
| claim_type: traditional_lineage |
| confidence: low_historical / high_traditional |
| sources: Autobiography of a Yogi; Kriya lineage oral records |
| notes: Not independently corroborated by external historical sources. |
| The claim originates within and is important to the Kriya Yoga tradition. |

| CLAIM SCHEMA |
| --- |
| claim { |
| id : UUID |
| subject_id : UUID |
| predicate : string |
| object : string | UUID |
| claim_type : traditional | doctrinal | hagiographic | scholarly |
| | archaeological | mythological | speculative | folk |
| confidence : high | medium | low | contested | unknown |
| source_ids : UUID[] |
| tradition_id : UUID? // which tradition makes this claim |
| counter_claims : UUID[] // claim IDs that dispute this |
| notes : string |
| citation_required : boolean |
| } |

## 3.4 Concept & Interpretation Layer

Concepts are first-class entities. The same concept — reincarnation, sacrifice, enlightenment — is expressed differently across traditions. Each interpretation is its own entity, linked to the parent concept and the tradition.

| Tradition | Concept: Reincarnation | Key Distinction | Terminal Goal |
| --- | --- | --- | --- |
| Hindu | Accepts | Ātman reincarnates across births | Moksha — liberation of the ātman |
| Buddhism | Accepts (qualified) | Causal continuity, no permanent self | Nirvāṇa — cessation of rebirth |
| Jainism | Accepts | Jīva (soul-substance) reincarnates | Mukti — liberation of the jīva |
| Sikhism | Accepts | Liberation through Naam; divine grace | Sachkhand — realm of truth |
| Platonism | Accepts | Immortal soul, purification cycle | Return to the Good / Forms |
| Kabbalah | Accepts (Gilgul) | Soul returns to complete tikkun | Completion of soul correction |
| Christianity | Generally rejects | Resurrection, not rebirth | Eternal life / resurrection body |
| Islam | Rejects | One life; resurrection and judgment | Paradise / al-Janna |
| Manichaeism | Accepts | Soul purification through rebirths | Return to Realm of Light |
| Pythagoreans | Accepts | Soul transmigration incl. animals | Escape from metempsychosis |

# 4. Navigation & Information Architecture

## 4.1 Top-Level Navigation

Navigation is organized into three zones: Explore (browsing), Research (scholarship), and Tools (computation and AI).

| EXPLORE |  |
| --- | --- |
| Traditions | Religions, schools, sects, movements, orders |
| Deities & Beings | Gods, spirits, angels, demons, mythic figures |
| Texts & Scriptures | Scriptures, commentaries, oral traditions |
| Practices | Meditation, ritual, prayer, initiation, pilgrimage |
| Figures | Founders, saints, prophets, mystics, scholars |
| Lineages | Guru-disciple chains, apostolic successions |
| Myths & Narratives | Creation myths, hero cycles, cosmogonic stories |
| Concepts | Karma, salvation, enlightenment, nonduality, grace |
| Symbols & Objects | Sacred symbols, ritual objects, iconographic systems |
| Places | Sacred sites, temples, regions, mythic realms |
| Timeline | Events, eras, world ages across traditions |
| Map | Geographic distribution, pilgrimage routes, sacred geography |
| RESEARCH |  |
| Articles | Long-form scholarly articles |
| Source Library | Primary sources, manuscripts, citations |
| Comparative Themes | Flood myths, dying gods, cosmic eggs across traditions |
| Disputed Claims | Contested historical and doctrinal claims with evidence |
| Scholarly Theories | Academic frameworks and interpretive hypotheses |
| Datasets & Exports | JSON-LD, RDF, CSV, IIIF manifests |
| TOOLS |  |
| Graph Explorer | Interactive relationship traversal |
| Lineage Builder | Visualize and trace lineage chains |
| Comparison View | Side-by-side entity and concept comparison |
| Comparative Mapping Engine | Deity/symbol/concept equivalence explorer with typed edges |
| Developmental Lens | View entities, traditions, and concepts by altitude/state across frameworks (§17) |
| AI Query / RAG Chat | Natural language retrieval over the corpus |
| Timeline Explorer | Filter and explore across time |
| Citation Browser | Source and provenance explorer |

## 4.2 Entity Page Structure

All entity pages share a consistent layout. Sections that have no content for a given entity are hidden.

| STANDARD ENTITY PAGE SECTIONS |
| --- |
| 1. Header: Canonical name · Alternate names · Type badge · Tradition(s) · Date range · Status |
| 2. Overview: Short description · Key relationships summary · Confidence indicator |
| 3. Full Description: Long-form encyclopedic text with inline citations |
| 4. Relationships: Visual graph + tabular list of all typed relationships |
| 5. Tradition-specific content: Practice, doctrine, lineage, interpretation |
| 6. Texts: Associated scriptures, commentaries, mentions |
| 7. Figures: Associated persons, founders, deities |
| 8. Places: Associated sacred sites, regions, mythic locations |
| 9. Timeline: Events and periods in historical context |
| 10. Symbols & Objects: Associated material and visual culture |
| 11. Claims & Disputes: All claims with confidence and sources visible |
| 12. Comparative Relationships: Typed cross-entity equivalences, parallels, and oppositions with full edge metadata |
| 13. Developmental Readings: Altitude / state / quadrant annotations across frameworks, each attributed (see §17) |
| 14. Images & Media: IIIF-compatible image gallery |
| 15. AI Summary: Pre-generated RAG-optimized summary |
| 16. Related Entities: Similar/connected entities |
| 17. Sources: Full citation list |

# 5. Places: Sacred Geography & Mythic Space

Places are not map points. They are meaning-clusters. A mountain, monastery, city, shrine, underworld, or heavenly realm all qualify as place entities — but with different levels of physical certainty and different layers of religious significance.

## 5.1 Place Taxonomy

| Place Type | Physical Certainty | Examples |
| --- | --- | --- |
| Sacred Natural Site | Definite location | Mount Sinai, Bodh Gaya, Mount Kailash, Delphi, Varanasi |
| Built Religious Site | Definite location | Hagia Sophia, Nalanda, Shaolin, Golden Temple, Angkor Wat |
| Pilgrimage Site / Route | Definite location | Camino de Santiago, Kumbh Mela sites, Hajj route |
| Historical Region | Approximate | Judea, Magadha, Tibet, Gandhara, Bactria, Mesopotamia |
| Archaeological Site | Located; meaning debated | Gobekli Tepe, Çatalhöyük, Mohenjo-daro |
| Mythic Cosmological Place | No physical location | Mount Meru, Valhalla, Olympus, Mictlan, Pure Land, Duat |
| Heavenly / Afterlife Realm | No physical location | Heaven, Jannah, Svarga, Pure Land, Elysium, Aaru |
| Underworld / Hell Realm | No physical location | Hades, Sheol, Naraka, Helheim, Mictlan, Tartarus |
| Eschatological Site | Future/symbolic | New Jerusalem, Shambhala, Saoshyant location |

## 5.2 Multi-Layer Significance

The same physical location can carry separate religious significance for multiple traditions. These are stored as distinct meaning layers, not merged.

| EXAMPLE: JERUSALEM |
| --- |
| Physical entity: City, modern Israel / Palestinian territories |
| Jewish sacred layer: Site of Temple Mount; holiest city; eschatological center |
| Christian sacred layer: Site of crucifixion, resurrection, Pentecost; eschatological New Jerusalem |
| Islamic sacred layer: Al-Quds; third holiest city; site of Isra and Miraj (Night Journey) |
| Symbolic/mythic layer: "Heavenly Jerusalem" — eschatological city in Revelation and Islamic tradition |
|  |
| Each layer = separate entity record linked to the physical place entity. |

## 5.3 Place Schema Extension

| PLACE SCHEMA |
| --- |
| place { |
| // inherits base entity schema |
| place_type : sacred_site | built_site | pilgrimage | region |
| | mythic_realm | cosmological | eschatological |
| physical_certainty : confirmed | approximate | symbolic | none |
| coordinates : { lat: float, lng: float }? |
| geometry : GeoJSON? |
| modern_country : string? |
| historical_region : string |
| geonames_id : string? |
| time_period { |
| founded : date? |
| active_period : DateRange? |
| destroyed : date? |
| current_status : active | ruins | lost | reconstructed | symbolic |
| } |
| significance_layers : SignificanceLayer[] // one per tradition |
| physical_equivalent : UUID? // for mythic places symbolically mapped to real sites |
| pilgrimage_data : { annual_visitors: int?, season: string?, route: UUID? }? |
| } |
|  |
| significance_layer { |
| tradition_id : UUID |
| significance_type : sacred | historical | mythological | eschatological | ancestral |
| description : string |
| associated_texts : UUID[] |
| associated_events : UUID[] |
| } |

# 6. Media & Image Archive

Images and artifacts are first-class entities — not attachments to other records. Each image record captures full provenance, iconographic metadata, and IIIF-compatible access.

| IMAGE RECORD SCHEMA |
| --- |
| image_record { |
| image_id : UUID |
| title : string |
| image_url : URL |
| iiif_manifest : URL? |
| thumbnail_url : URL |
| depicted_entities : { entity_id: UUID, role: string }[] |
| tradition_ids : UUID[] |
| date_range : DateRange |
| date_certainty : confirmed | approximate | disputed | unknown |
| region : string |
| medium : string // e.g. "Thangka painting", "Bronze sculpture" |
| dimensions : { height: float, width: float, unit: string }? |
| source_institution : string |
| accession_number : string? |
| license : CC0 | CC_BY | CC_BY_SA | fair_use | rights_reserved | unknown |
| caption : string |
| iconographic_tags : string[] |
| visual_description : string // AI-generated alt text / description for retrieval |
| related_articles : UUID[] |
| embedding : vector // visual embedding for similarity search |
| } |

| Image Category | Examples | Priority |
| --- | --- | --- |
| Deity iconography | Statues, thangkas, icons, reliefs, murals | High |
| Sacred manuscripts | Illuminated texts, scrolls, tablets | High |
| Ritual scenes | Ceremonies, initiations, pilgrimage | High |
| Sacred sites | Temples, shrines, sacred geography | High |
| Symbolic art | Mandalas, yantra, geometric sacred art | Medium |
| Artifacts | Ritual objects, votive objects, amulets | Medium |
| Portraits | Religious figures, saints, sages | Medium |
| Maps | Historical sacred geography, pilgrimage maps | Medium |
| Coins & inscriptions | Epigraphic evidence, numismatic sources | Low–Medium |

# 7. RAG & AI Training Architecture

## 7.1 Retrieval Chunk Strategy

Each entity generates multiple retrieval chunks — one per semantic dimension. This enables precise retrieval without forcing a model to parse a monolithic article.

| Chunk Type | Contents | Avg Tokens |
| --- | --- | --- |
| canonical_summary | Identity, type, tradition, dates, key facts | 150–300 |
| historical_summary | Historical context, origins, dating, archaeology | 200–500 |
| doctrinal_summary | Beliefs, teachings, theological positions | 200–500 |
| lineage_summary | Teacher-student chains, transmission history | 150–400 |
| practice_summary | Rituals, meditation, worship, pilgrimage | 150–400 |
| narrative_summary | Myths, stories, hagiographic accounts | 200–600 |
| concept_interpretation | How a concept is understood within a specific tradition | 150–300 |
| comparative_entry | Cross-tradition comparison of an entity or concept | 300–700 |
| dispute_summary | Contested claims, scholarly debates, uncertainties | 150–400 |
| source_notes | Key textual and archaeological sources | 100–300 |
| image_caption | Description and iconographic significance of images | 100–200 |
| timeline_entry | Date-anchored event or period description | 80–200 |
| relationship_explanation | Narrative explanation of key relationships | 100–300 |

## 7.2 RAG Chunk Metadata

Every chunk carries structured metadata used for filtered retrieval.

| RAG CHUNK SCHEMA |
| --- |
| rag_chunk { |
| chunk_id : UUID |
| entity_id : UUID |
| chunk_type : ChunkType // see table above |
| text : string // the retrieval-optimized text |
| embedding : vector[] // dense vector(s) |
| sparse_tokens : string[] // for hybrid search |
| metadata { |
| entity_type : EntityType |
| tradition_ids : UUID[] |
| region : string[] |
| date_range : DateRange |
| source_ids : UUID[] |
| confidence : ConfidenceLevel |
| claim_type : ClaimType |
| tags : string[] |
| language : string // language of original source |
| citation_required : boolean |
| is_disputed : boolean |
| } |
| } |

## 7.3 Retrieval Architecture

| Component | Technology Options | Purpose |
| --- | --- | --- |
| Vector store | Pinecone, Weaviate, pgvector, Qdrant | Dense semantic similarity search |
| Sparse index | Elasticsearch, OpenSearch, BM25 | Keyword and entity-name retrieval |
| Hybrid reranker | Cohere Rerank, cross-encoder, ColBERT | Combine dense + sparse scores |
| Graph store | Neo4j, Amazon Neptune, ArangoDB | Relationship traversal and reasoning |
| Relational store | PostgreSQL | Structured entity records, claims, metadata |
| Object storage | S3 / R2 / GCS | Images, PDFs, audio, video |
| Search index | Elasticsearch / Typesense | Full-text and faceted search |
| Cache layer | Redis | Frequent entity lookups, graph traversals |

# 8. Knowledge Graph Model

## 8.1 Graph Architecture

The knowledge graph is the connective tissue of the entire system. All entity records are nodes; all relationship records are edges. The graph enables traversal, inference, and comparative analysis that flat databases cannot support.

| GRAPH TRAVERSAL EXAMPLE: "Reincarnation" |
| --- |
| Concept: Reincarnation |
| ├── supported_by → [Hinduism, Buddhism, Jainism, Sikhism, Manichaeism, Kabbalah, Pythagoreanism] |
| ├── rejected_by → [Sunni Islam, most of Christianity, secular materialism] |
| ├── qualified_by → [Druze (yes), Reform Judaism (no), Christian Science (no)] |
| ├── related_to → [Karma, Samsara, Moksha, Nirvana, Jiva, Atman, Anatman] |
| ├── opposed_by → [Resurrection, Final Judgment, Annihilationism] |
| ├── attested_in → [Bhagavad Gita, Upanishads, Phaedrus, Tibetan Book of the Dead, |
| │ Jataka Tales, Zohar] |
| ├── figures → [Buddha, Yajnavalkya, Plato, Pythagoras, Mani, Origen (disputed)] |
| └── motif → [Er Myth, Jataka Tales, Bardo Narratives, Gilgul stories] |

## 8.2 Graph Node Labels

In the graph database, node labels map directly to entity types. Nodes carry a subset of their full relational schema as properties for fast traversal.

| Graph Label | Key Properties on Node | Primary Edge Types |
| --- | --- | --- |
| Tradition | name, dates, region, confidence | SUBTRADITION_OF, FOUNDED_BY, INFLUENCED_BY |
| Concept | name, concept_family, first_attested | RELATED_TO, OPPOSED_BY, TRANSCENDED_BY |
| ConceptInterpretation | tradition_id, position, goal | INTERPRETATION_OF, HELD_BY |
| Figure | name, dates, role, status | TEACHER_OF, MEMBER_OF, ATTESTED_IN |
| Deity | name, pantheon, domain, status | DEITY_IN, CONSORT_OF, CHILD_OF |
| Text | title, type, date, canonical_for | COMMENTARY_ON, COMPOSED_BY, CANON_OF |
| Myth | title, tradition, motif_ids | CONTAINS_MOTIF, DEPICTS, PARALLEL_TO |
| Motif | name, type, first_attested | EXEMPLIFIED_BY, RELATED_MOTIF |
| Place | name, type, coordinates, certainty | LOCATED_IN, PILGRIMAGE_FOR, MYTHIC_EQ |
| Practice | name, type, tradition | PRACTICE_OF, REQUIRES, AIMS_AT |
| Claim | type, confidence, tradition | ASSERTS, DISPUTED_BY, SUPPORTED_BY |

# 9. Concept Ontology

Concepts are the most analytically powerful entity type. They are cross-traditional nodes that enable comparative religion at scale. The concept ontology is organized into families.

## 9.1 Afterlife Concept Family

| Category | Concept Entities |
| --- | --- |
| Processes | Reincarnation · Resurrection · Metempsychosis · Soul migration · Judgment · Dissolution |
| Positive Realms | Heaven · Jannah · Svarga · Pure Land · Valhalla · Elysium · Aaru · Tlalocan · Sukhavati |
| Negative Realms | Hell · Jahannam · Naraka · Helheim · Tartarus · Mictlan · Gehenna |
| Intermediate Realms | Purgatory · Bardo · Limbo · Sheol · Hades · Ghost realm · Ancestor realm |
| Liberation States | Nirvāṇa · Moksha · Mukti · Theosis · Union with God · Fanaa |
| Eschatological Agents | Psychopomps · Angels of death · Osiris · Yama · Azrael |
| Cosmological Frameworks | Samsara · Buddhist 31 realms · Hindu lokas · Norse 9 worlds · Gnostic aeons |

## 9.2 Major Concept Families

| Concept Family | Sample Concepts | Cross-Traditional Reach |
| --- | --- | --- |
| Afterlife | Reincarnation, Resurrection, Nirvana, Heaven, Bardo | Universal |
| Cosmogony | Creation, Chaos, Ex nihilo, Emanation, Cosmic Egg | Universal |
| Soteriology | Salvation, Liberation, Enlightenment, Grace, Merit | Universal |
| Ethics & Causation | Karma, Sin, Dharma, Virtue, Fate, Predestination | Near-universal |
| Ontology | Atman, Brahman, Anatman, Void, Logos, Tao, Nonduality | Widespread |
| Sacred Power | Mana, Shakti, Baraka, Prana, Chi, Ruach, Pneuma | Widespread |
| Divine Mediation | Avatar, Messiah, Bodhisattva, Prophet, Incarnation | Widespread |
| Ritual Efficacy | Sacrifice, Prayer, Mantra, Sacrament, Offering, Vow | Universal |
| Sacred Knowledge | Gnosis, Jnana, Prajna, Revelation, Illumination | Widespread |
| Mystical States | Samadhi, Satori, Theosis, Fana, Union, Rapture | Widespread |
| Sacred Time | World ages, Kali Yuga, Apocalypse, Millennium, Mappo | Widespread |
| Social Structure | Caste, Sangha, Ummah, Church, Tribe, Covenant people | Widespread |

# 10. Mythological Motifs

Motifs are recurring narrative patterns that appear across geographically and historically separate traditions. They are one of the most powerful comparative layers in the system.

| Motif | Key Traditions / Examples | Comparative Notes |
| --- | --- | --- |
| The Great Flood | Mesopotamian, Hebrew, Hindu, Greek, Mesoamerican | Utnapishtim · Noah · Manu · Deucalion · Viracocha |
| Dying & Rising God | Egyptian, Canaanite, Phrygian, Christian | Osiris · Baal · Attis · Jesus (debated category) |
| Virgin / Miraculous Birth | Hindu, Buddhist, Christian, Egyptian, Greek | Krishna · Buddha · Jesus · Horus · Perseus |
| Cosmic Egg | Hindu, Orphic, Finnish, Chinese, Egyptian | Hiranyagarbha · Orphic Phanes · Cosmic Mundane Egg |
| World Tree / Axis Mundi | Norse, Siberian, Hindu, Mesoamerican | Yggdrasil · Ashvattha · Mount Meru analogue |
| Divine Twins | Roman, Greek, Vedic, Iranian, Mesoamerican | Romulus & Remus · Ashvins · Yima |
| Trickster | Native American, Norse, West African, Greek | Coyote · Loki · Anansi · Hermes |
| Dragon / Serpent Slayer | Indo-European, Semitic, East Asian | Indra · Marduk · St. George · Thor · Perseus |
| Hero's Journey | Universal — Gilgamesh to Buddha to Moses | Campbell's monomyth — departure, initiation, return |
| The Trickster Teacher | Sufi tales, Zen koans, Taoist parables | Nasreddin · Mulla stories · Zen masters |
| Sacred Mountain | Hindu, Greek, Mesopotamian, Mesoamerican | Meru · Olympus · Ziggurat · Teotihuacan |
| Primordial Sacrifice | Vedic, Norse, Aztec, Mesopotamian | Purusha · Ymir · Quetzalcoatl · Marduk/Tiamat |

# 11. Technology Stack & Implementation

## 11.1 Storage Layer

| Layer | Technology | Role |
| --- | --- | --- |
| Primary relational | PostgreSQL 16+ | All entity records, claims, citations, metadata |
| Graph database | Neo4j or Amazon Neptune | Relationship traversal, motif pattern matching, lineage tracing |
| Vector store | pgvector (integrated) or Pinecone | RAG dense retrieval, semantic similarity |
| Search index | Elasticsearch / Typesense | Full-text, faceted, entity-name search |
| Object storage | S3-compatible (R2, GCS, S3) | Images, PDFs, audio, video, IIIF tiles |
| Cache | Redis | Hot entity lookups, computed relationship summaries |
| Linked data export | RDF / JSON-LD / SPARQL endpoint | External scholarly consumption, Wikidata sync |

## 11.2 Confidence & Provenance System

Every data point carries explicit provenance. The system never silently asserts a fact.

> **Canonical encoding.** Confidence is stored as a numeric `confidence` ∈ [0.0, 1.0] (the Mythographica
> assertion convention) with the qualitative band below **derived** from it
> (`≥0.8 high · 0.55–0.79 medium · 0.3–0.54 low · <0.3 speculative`). `tradition_specific` and
> `contested` are orthogonal flags derived from `claim_type` / `is_disputed`, not from the score. See
> core meta-model §3.2 for the full reconciliation table.

| Confidence Level | Meaning | Example |
| --- | --- | --- |
| high | Multiple independent scholarly sources agree | Buddha lived c. 5th–4th century BCE in northeastern India |
| medium | General scholarly consensus with some debate | Exact dates of Zoroaster; location of his origin |
| low | Limited or contested evidence | Pythagoras's specific doctrines (all second-hand) |
| traditional_only | Asserted within a tradition; no external corroboration | Mahavatar Babaji as historical person |
| speculative | Scholarly hypothesis; significant opposition exists | Zoroastrian origins of Jewish afterlife concepts |
| disputed | Directly contradicted by major scholarly positions | Dates of Exodus as literal historical event |

## 11.3 Editorial Workflow

- Domain experts (religion, archaeology, linguistics) create and review entity records
- Claims are tagged at point of entry with type, confidence, and source
- AI assists in generating RAG chunks, alternative name extraction, and relationship suggestions
- All AI-generated content is reviewed before publication
- Community editors can flag disputed claims via structured dispute mechanism
- Senior editors adjudicate disputes; resolution is stored as its own record
- Entities are versioned; all changes are auditable

# 12. Phased Implementation Roadmap

| Phase | Focus | Key Deliverables | Duration |
| --- | --- | --- | --- |
| 0 — Foundation | Infrastructure | DB schema, graph model, claim model, API, admin CMS, editorial workflow | 2–3 months |
| 1 — Core Corpus | Major traditions | 12 major world religions: entities, relationships, claims, sources | 4–6 months |
| 2 — Concept Layer | Cross-traditional | All major concept families, motifs, interpretation tables, experience states | 3–4 months |
| 3 — Comparative Layer | Cross-entity equivalences | Full comparative edge schema, predicate vocabulary, Deity/Symbol/Concept equivalence maps | 3–4 months |
| 4 — Deep Traditions | Subtraditions | Schools, sects, lineages, minor traditions, indigenous religions | 6–9 months |
| 5 — Media Archive | Image corpus | IIIF-compatible image records, iconography tagging, visual embeddings | 4–6 months |
| 6 — Text Layer | Scriptures | Text entities with chapter/verse structure for citation-level RAG | 4–6 months |
| 7 — Source Library | Provenance | Full source entities, manuscript records, archaeological evidence | 3–4 months |
| 8 — Governance | Editorial platform | Scholar review workflow, dispute resolution, tradition reviewer program, AI curation pipeline | 2–3 months |
| 9 — AI & Export | AI products | Public RAG chat, dataset exports, API, SPARQL endpoint, comparative dossier generator | 2–3 months |

# 13. Summary Architecture

| THE COMPLETE SYSTEM IN ONE STATEMENT |
| --- |
| Build it as: Wikidata (claim-based graph) + Stanford Encyclopedia (long-form scholarship) |
| + a lineage graph (teacher-student chains) + a museum archive (IIIF image system) |
| + a RAG-ready document corpus (chunked, embedded, metadata-tagged) |
| + a motif database (recurring cross-cultural patterns) |
| + an experience state library (samadhi, satori, mystical union, possession) |
| + a concept interpretation engine (same concept, tradition-specific readings) |
| + a comparative mapping engine (typed, claim-based cross-entity equivalences) |
|  |
| Connected by an explicit claim layer that always distinguishes: |
| "Tradition X asserts Y" from "Scholarship demonstrates Y" from "Y is debated" |
| "Hermes is functionally equivalent to Thoth in Hellenistic context" from "Hermes IS Thoth" |

**The four additions with the highest long-term AI value:** Claims (provenance-tagged assertions with full confidence metadata), Motifs (recurring cross-cultural narrative patterns), Experience States (reported states of consciousness), and Comparative Relationship Edges (typed, time-bounded, tradition-scoped equivalences and parallels). Most religion databases have entities. Very few model what traditions claim, which narrative patterns recur, which states practitioners report, and how entities in different traditions relate without collapsing nuance. Those four layers are where comparative insight emerges — and where the largest AI reasoning gains will be found.

# 14. Comparative Relationship Layer

Most knowledge graphs flatten cross-traditional connections into a single "equivalent to" or "related to" edge. This destroys the scholarly nuance that makes comparative religion meaningful. The comparative relationship layer treats every cross-entity comparison as a richly attributed, claim-based edge — with a type, a tradition perspective, a time frame, a confidence level, similarities, differences, and sources.

| THE CORE PROBLEM |
| --- |
| A simple "owl:sameAs" or "equivalent_to" edge cannot express: |
| — that Hermes = Thoth is culturally bounded (Hellenistic Egypt only) |
| — that the equivalence is temporally specific (c. 300 BCE – 400 CE) |
| — that modern scholarship qualifies it (functional parallel, not identity) |
| — that Thoth has a lunar aspect with no Hermetic parallel |
|  |
| The rich comparative edge preserves the full argument so AI and researchers |
| can reason over it — not just retrieve a binary link. |

## 14.1 Comparative Edge Schema

Every comparative relationship is stored as a first-class object, not a simple predicate.

| COMPARATIVE EDGE SCHEMA |
| --- |
| comparative_relationship { |
| comparison_id : UUID |
| subject_entity_id : UUID |
| predicate : ComparativePredicateType // see §14.2 |
| object_entity_id : UUID |
|  |
| // Nature of the comparison |
| comparison_type : interpretatio_graeca | typological | syncretic | diffusionist |
| | functional | iconographic | conceptual | scholarly_hypothesis |
| comparison_scope : string // e.g. "messenger function and writing domain" |
|  |
| // Who asserts this? |
| tradition_context : string // e.g. "Hellenistic_Egyptian_syncretism" |
| perspective : string // e.g. "Greek interpretation of Egyptian deities" |
| asserted_by : string[] // persons, texts, or scholarly traditions |
| scholarly_consensus : widely_accepted | debated | minority_view | rejected |
|  |
| // Temporal and geographic scope |
| time_period : DateRange |
| region : string[] |
|  |
| // Confidence |
| confidence : high | medium | low | disputed | tradition_specific |
| disputed : boolean |
| counter_claim_ids : UUID[] |
|  |
| // Substance of the comparison |
| similarities : string[] // specific shared attributes or functions |
| differences : string[] // specific divergences that limit the equivalence |
|  |
| // Sources |
| primary_source_ids : UUID[] |
| secondary_source_ids : UUID[] |
| notes : string |
| } |

## 14.2 Comparative Predicate Vocabulary

A controlled vocabulary of comparative predicates replaces the generic "related to" catch-all. Each predicate has precise usage guidelines editors follow for consistency.

### Deities & Supernatural Beings

| Predicate | Meaning | Example |
| --- | --- | --- |
| comparatively_equivalent_to | Explicit syncretic identification across traditions | Hermes ≈ Thoth (Hellenistic Egypt) |
| typological_parallel | Same archetypal function, no historical connection | Indra (thunder) and Zeus (thunder) |
| derived_from | One deity originated through cultural diffusion | Serapis derived from Osiris-Apis |
| syncretically_merged_into | Two deities combined into a new form | Hermanubis (Hermes + Anubis) |
| opposed_to_in_narrative | Mythic antagonist parallels across traditions | Thor vs. Jormungandr || Indra vs. Vritra |
| associated_with_same_symbol | Share a dominant symbol without identity claim | Quetzalcoatl and Kukulkan (feathered serpent) |
| scholarly_contested_identification | Proposed link is actively debated in scholarship | Yahweh and Aten; Moses and Akhenaten |
| iconographic_variant_of | Different name, nearly identical visual program | Regional deity variants in Hinduism |

### Symbols, Motifs & Iconography

| Predicate | Meaning | Example |
| --- | --- | --- |
| identical_morphology | Same visual form, different or contested meaning | Swastika: Hindu auspiciousness vs. Nazi appropriation |
| shared_motif_cluster | Belong to same motif family | Yggdrasil, Ashvattha, Cross as world tree |
| functional_equivalent_in_ritual | Used analogously in ritual contexts | Lingam and Omphalos (cosmic axis stones) |
| convergent_independent_origin | Similar form arose independently | Pyramid forms in Mesoamerica and Egypt |
| appropriated_or_contested | Meaning radically changed across cultures | Cross: pre-Christian sun symbol to Christian symbol |
| iconographically_influenced_by | Artistic borrowing or influence pathway | Buddhist nimbus/halo and later Christian halo |

### Concepts & Doctrines

| Predicate | Meaning | Example |
| --- | --- | --- |
| functional_equivalent | Analogous role in soteriology or cosmology | Moksha and Nirvana (both liberation states) |
| partial_overlap | Overlapping but not identical in scope or meaning | Christian Logos vs. Stoic Logos |
| direct_borrowing | Historical influence is probable or demonstrated | Jewish resurrection and Zoroastrian Frashokereti |
| universal_theme | Similar concept in many unrelated traditions | Flood myth; the Golden Rule; sacred marriage |
| opposing_concepts | Systems explicitly reject each other | Reincarnation vs. bodily Resurrection |
| terminological_cognate | Same etymological root, divergent meanings | Sanskrit deva and Latin deus |
| eschatological_parallel | Structurally similar end-times narratives | Ragnarok and Revelation |

## 14.3 Multi-Claim Dispute Handling

When traditions or scholarly schools disagree on a comparison, the system stores multiple competing claims — it does not adjudicate. Both claims are surfaced to users and AI.

| EXAMPLE: INANNA AND ISHTAR — TWO CLAIMS STORED IN PARALLEL |
| --- |
| CLAIM A (Traditional theological synthesis): |
| subject: Inanna | predicate: comparatively_equivalent_to | object: Ishtar |
| perspective: Babylonian theological synthesis |
| confidence: traditional_acceptance |
| time_period: Old Babylonian period onwards |
|  |
| CLAIM B (Modern assyriology): |
| subject: Inanna | predicate: typological_parallel | object: Ishtar |
| perspective: modern_assyriology |
| confidence: scholarly_consensus |
| note: Not direct identity; Ishtar absorbed Inanna's traits over centuries. |
| The relationship is historical absorption, not synchronic equivalence. |
|  |
| Both claims are surfaced — neither is suppressed. |
| AI responses must reflect which claim answers which question in which context. |

## 14.4 Graph Database Implementation

In Neo4j, comparative relationships are edge properties on a dedicated COMPARATIVE_EQUIVALENCE relationship type. In PostgreSQL, they live in a comparative_relationships table. Both can be queried and filtered.

| NEO4J GRAPH IMPLEMENTATION |
| --- |
| // Neo4j Cypher pattern |
| (:Deity {name: "Thoth"}) |
| -[comp:COMPARATIVE_EQUIVALENCE { |
| comparison_id: "cmp_001", |
| predicate: "comparatively_equivalent_to", |
| comparison_type: "interpretatio_graeca", |
| tradition_perspective: "Greek_Hellenistic", |
| time_period_start: -300, |
| time_period_end: 400, |
| confidence: "high_historical", |
| scholarly_consensus: "widely_accepted_in_period_context", |
| similarities: ["messenger", "writing", "magic", "psychopomp"], |
| differences: ["Thoth lunar aspect", "ibis form has no Hermes parallel"], |
| source_ids: ["plutarch_de_isis", "corpus_hermeticum"], |
| notes: "Interpretatio Graeca; became standard in Ptolemaic Egypt" |
| }] |
| ->(:Deity {name: "Hermes"}) |

## 14.5 UI: Comparative Mapping Views

The comparative relationship layer enables dedicated UI views not possible with simple edges.

| View | Description | Powered By |
| --- | --- | --- |
| Deity Equivalence Map | Graph where edges are colored by type and confidence; filter by era or tradition | Comparative edges + time filter |
| Comparative Symbol Table | For any symbol: all traditions, meanings, morphological variants, contested status | Comparative + symbol entities |
| Scholarly Claim Tracker | For any disputed link: all claims pro/con with full evidence dossier | Multi-claim storage |
| Time-Aware Similarity Slider | Show only equivalences as understood in a given century | time_period qualifiers on edges |
| Concept Comparison Panel | Side-by-side: how two traditions handle the same concept | Concept interpretations + comparative edges |
| Comparative Dossier | Any two entities: auto-generated structured report of similarities, differences, claim history | Full comparative edge metadata |

## 14.6 AI Retrieval with Comparative Edges

When a RAG query asks a comparative question, the retrieval pipeline uses comparative edge metadata to generate source-grounded, nuance-preserving answers.

| EXAMPLE: "How is Hermes related to Thoth?" |
| --- |
| RAG pipeline: |
| 1. Locate comparative_equivalence edge between Hermes and Thoth |
| 2. Retrieve all edge qualifiers: type, period, tradition, similarities, differences, sources |
| 3. Retrieve supporting RAG chunks: Hellenistic context, Hermetic texts, Plutarch |
| 4. Retrieve any counter-claim chunks (modern scholarly qualification) |
|  |
| AI output template: |
| "According to Hellenistic syncretic tradition (c. 300 BCE – 400 CE), Hermes was |
| identified with the Egyptian god Thoth, sharing functions as god of writing, magic, |
| and guide of souls. This identification is attested in Plutarch and the Hermetic corpus. |
| However, modern scholars note that Thoth's lunar aspect and ibis iconography have no |
| direct parallel in classical Hermes, making this a functional equivalence within a |
| specific historical context rather than an identity claim." |
|  |
| The AI never states: "Hermes is Thoth." |

# 15. Claim Model: Full Specification

The claim model is the most architecturally critical layer in the system. It is what separates a claim-aware knowledge graph from a naive fact database. Every major assertion — historical, doctrinal, mythological, or comparative — is stored as a structured claim with full provenance.

## 15.1 Why Claims Are Not Facts

| THE EPISTEMIC PROBLEM ALL RELIGION DATABASES FACE |
| --- |
| These four statements look the same in a naive database. They are fundamentally different: |
|  |
| 1. "Lahiri Mahasaya lived 1828–1895" |
| → Historical fact. Birth and death records. Confidence: HIGH. |
|  |
| 2. "Mahavatar Babaji taught Lahiri Mahasaya" |
| → Traditional lineage claim. Source: Autobiography of a Yogi (hagiographic). |
| No independent historical corroboration. Confidence: TRADITION-SPECIFIC. |
|  |
| 3. "The Exodus occurred under Ramesses II" |
| → Scholarly hypothesis. Widely held but not archaeologically confirmed. |
| Confidence: MEDIUM / DEBATED. |
|  |
| 4. "Osiris was resurrected by Isis" |
| → Mythological narrative. Not a historical or doctrinal claim. |
| Confidence: NOT APPLICABLE (myth category). |
|  |
| A system that stores all four the same way will generate unreliable AI answers. |

## 15.2 Full Claim Schema

| FULL CLAIM SCHEMA |
| --- |
| claim { |
| id : UUID |
|  |
| // The assertion |
| subject_id : UUID |
| predicate : string |
| object : string | UUID |
|  |
| // Claim classification |
| claim_type : historical | mythological | doctrinal | hagiographic |
| | traditional | archaeological | scholarly | symbolic |
| | comparative | disputed | folk |
|  |
| // Confidence |
| confidence : high | medium | low | tradition_specific |
| | contested | speculative | unknown |
|  |
| // Provenance |
| source_ids : UUID[] // primary sources |
| secondary_source_ids : UUID[] // secondary/scholarly sources |
| tradition_id : UUID? // which tradition makes this claim |
| asserted_by : string[] // persons or bodies asserting |
|  |
| // Scope |
| date_range : DateRange? |
| region : string[]? |
| tradition_context : string? |
|  |
| // Dispute handling |
| is_disputed : boolean |
| counter_claim_ids : UUID[] // IDs of claims that contest this one |
| dispute_notes : string? |
|  |
| // Editorial |
| citation_required : boolean |
| editorial_notes : string? |
| reviewed_by : string? |
| review_date : date? |
| } |

## 15.3 Claim Type Reference

| Claim Type | Definition | AI Output Phrasing |
| --- | --- | --- |
| historical | Attested by independent, contemporaneous, or archaeological sources | "Historically, X..." |
| mythological | Narrative content within a tradition's sacred stories | "In [tradition] mythology, X..." |
| doctrinal | Formally taught or defined by a tradition or institution | "[Tradition] teaches that X..." |
| hagiographic | Appears in devotional biographies; may blend history and legend | "Devotional sources record that X..." |
| traditional | Preserved within a tradition; not independently corroborated | "According to [tradition], X..." |
| archaeological | Supported by physical evidence, but interpretation may vary | "Archaeological evidence suggests X..." |
| scholarly | Academic hypothesis with supporting argument | "Scholars have proposed that X..." |
| comparative | Cross-traditional comparison with typed relationship | "[Tradition A] identified X with Y in context Z..." |
| disputed | Active scholarly or traditional disagreement | "It is debated whether X..." |
| symbolic | Interpreted as symbolic or allegorical, not literal | "Symbolically, X represents..." |

# 16. Editorial & Governance Layer

A knowledge graph of this scope requires a serious, structured editorial workflow. The quality of the claim layer depends entirely on the rigor of the editorial process. Without it, the database will gradually accumulate uncategorized assertions that erode AI reliability.

## 16.1 Editorial Roles

| Role | Permissions | Responsibilities |
| --- | --- | --- |
| Contributor | Create drafts; add claims with sources; flag issues | Primary data entry; must cite sources for all claims |
| Domain Editor | Publish entities; edit claims; assign claim types and confidence | Subject-matter review within a tradition or domain |
| Scholar Reviewer | Approve/reject scholarly confidence ratings; add counter-claims | Academic quality control; dispute adjudication |
| Tradition Reviewer | Flag culturally sensitive content; validate tradition-specific claims | Insider perspective; prevents misrepresentation |
| Comparative Specialist | Create and approve comparative relationship edges | Cross-traditional equivalence and typology review |
| AI Curator | Review and approve AI-generated RAG chunks; check for hallucination | Ensures RAG corpus is accurate and appropriately hedged |
| Administrator | Full system access; merge/split proposals; schema changes | System governance; escalation point for disputes |

## 16.2 Entity Status Workflow

| EDITORIAL WORKFLOW SCHEMA |
| --- |
| entity_status: draft → under_review → published → flagged → archived |
|  |
| entity_quality_flags { |
| source_completeness_score : 0–100 |
| confidence_score : 0–100 |
| is_disputed : boolean |
| needs_citation : boolean |
| has_pending_merge : boolean |
| has_pending_split : boolean |
| tradition_reviewed : boolean |
| scholar_reviewed : boolean |
| ai_chunks_approved : boolean |
| last_full_review_date : date |
| } |
|  |
| change_log { |
| entity_id : UUID |
| changed_by : user_id |
| change_type : create | edit | claim_add | claim_dispute | status_change | merge | split |
| timestamp : datetime |
| diff : JSON |
| note : string |
| } |

## 16.3 Dispute Resolution Process

- A contributor or editor flags a claim as disputed and files a dispute record
- The dispute record cites the counter-sources and specifies the nature of disagreement
- Both the original claim and the counter-claim remain visible with dispute_flag = true
- A Scholar Reviewer or Tradition Reviewer reviews both sides
- Resolution options: retain both claims (most common), update confidence level, deprecate one claim with editorial note
- Resolution is stored as its own record — the dispute history is never deleted
- AI RAG chunks for disputed entities are flagged citation_required: true and include dispute summary

| EDITORIAL QUALITY PRINCIPLE |
| --- |
| The system should never aspire to a single authoritative truth on contested matters. |
| Its goal is to represent the full landscape of claims, perspectives, and evidence — |
| and to give AI and human researchers the metadata to navigate that landscape accurately. |
|  |
| A disputed claim, properly attributed, is more valuable than a false certainty. |

# 17. Integral / Developmental Layer

This is the layer that makes Kosmographica more than a comparative-religion encyclopedia. The full
schema is defined once, for all modules, in the [Core Meta-Model §4](../core-meta-model.md#4-developmental-integral-layer);
this section gives the Religion & Mythology module's usage. The developmental layer lets any
entity, claim, text, practice, figure, or movement be read through a developmental framework — and,
critically, **every such reading is itself a claim** (interpretive and contestable), carrying
`confidence`, `asserted_by`, and `sources`. The system never asserts an altitude as a fact.

## 17.1 What the layer adds

- **`DevelopmentalFramework`** — AQAL, Spiral Dynamics, Gebser's structures of consciousness,
  Fowler's stages of faith, Kohlberg, etc. (Authors link to `Historical Figure` entities.)
- **`DevelopmentalStage` / Altitude** — stages within a framework, each mapped to a shared
  cross-framework `altitude` key (archaic · magic · mythic · rational · pluralistic · integral · …)
  so traditions and figures can be compared *across* frameworks. Cross-framework equivalences are
  comparative claims, never identity.
- **`DevelopmentalAnnotation`** — attachable to any entity or claim, carrying `framework_id`,
  `stage_id` (vertical structure-stage), `state` (gross/subtle/causal/nondual), `quadrant`
  (AQAL interior/exterior × individual/collective), and `line` (cognitive, moral, spiritual,
  aesthetic, …).

## 17.2 State × Stage (Wilber–Combs) is kept distinct

The module enforces the Wilber–Combs distinction: a mystical **state** (the spec's `Experience State`
entity — samādhi, satori, mystical union) can be accessed at any developmental **stage**, but is
*interpreted* through that stage's structure. The two axes are modeled separately:

| EXAMPLE: SAME STATE, DIFFERENT STAGE-INTERPRETATIONS |
| --- |
| Experience State: mystical union (a subtle/causal state) |
| · interpreted at a mythic-membership stage → "union with a personal God of my tradition" |
| · interpreted at a rational stage → "an altered brain state / psychological peak experience" |
| · interpreted at a pluralistic stage → "a universal spiritual experience common to all faiths" |
| · interpreted at an integral stage → "non-dual awareness that includes and transcends prior framings" |
|  |
| Each row is a separate DevelopmentalAnnotation claim with its own asserted_by + confidence. |

## 17.3 Module usage notes

- **Traditions and concepts** may carry multiple developmental readings (e.g. a single tradition read
  as predominantly mythic by one interpreter and as having an integral contemplative core by another).
  Surface all readings; never collapse to one.
- **Concept interpretations** (§3.4) and developmental annotations compose: the same concept
  (reincarnation, grace) can be tagged with both a tradition-specific interpretation and an altitude.
- **AI / RAG** uses the layer to present *multiple developmental readings* and, where appropriate, to
  meet a questioner at their altitude — always attributing each reading, never asserting one as truth.
- **Provenance discipline** is identical to the Claim layer: a developmental reading without an
  `asserted_by` interpreter/school and a source is a draft, not a publishable annotation.

# 18. Federation & Source Systems

As a Kosmographica module, Religion & Mythology data federates with sibling source systems rather
than living in a silo (see [Core Meta-Model §6](../core-meta-model.md#6-federation--entity-resolution)).

- Every record carries a `source_system` and keeps its native key; a canonical Kosmographica ID
  (KID) is the join target, with `sameAs` reconciliation mapping native IDs (e.g. Mythographica
  `norse_odin`, a Sacred-Lineage `Figure`, a time-thread event, Wikidata `Q…`) to one entity.
- The claim/assertion model here is the **same** model implemented in Mythographica (numeric
  confidence, methodology, sources) — not a parallel one.
- Lineage transmission chains integrate the Sacred-Lineage (Kechimyaku) schema; the historical
  chronology integrates the time-thread timeline; the developmental frameworks integrate Kosmotheon.
- Ingestion **orchestrates** the existing loaders (Mythographica `seed_from_json.py`, Sacred-Lineage
  `db:import-legacy`) rather than replacing them.

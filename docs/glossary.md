# Glossary

> **Status:** stub (living) · Part of the [spec plan](./PLAN.md). Shared terminology so all
> contributors and docs use words the same way. Add terms as they stabilize.

| Term | Definition |
|---|---|
| **Kosmographica** | The umbrella system: a federated, claim-based knowledge graph aiming at a total record of human thought, culture, development, and history through an integral developmental lens. |
| **Engine** | The `kosmographica-engine` codebase — federation, storage, API, retrieval — that ingests source datasets into the canonical core. |
| **Core (meta-model)** | The thin universal schema (Entity, Claim, Relationship, Source, DevelopmentalAnnotation, TemporalAnchor, SpatialAnchor) shared by all modules. See [`core-meta-model.md`](./core-meta-model.md). |
| **Module** | A domain extension of the core (Religion & Mythology, Philosophy & Science, …) that adds entity subtypes and vocabulary but never redefines core fields. |
| **Entity** | Any node in the graph (a deity, person, text, concept, place, event, …). |
| **Claim / Assertion** | A provenanced, confidence-rated statement (subject–predicate–object). The system stores claims, not bare facts. "Assertion" is Mythographica's term for the same thing. |
| **Confidence** | Canonical numeric strength of a claim, 0.0–1.0, with a derived qualitative band (high/medium/low/…). See core §3.2. |
| **Comparative edge** | A typed, time- and tradition-scoped cross-entity relationship (equivalence, parallel, opposition) with similarities/differences — never a bare "same as." |
| **Developmental annotation** | A claim-grade reading of an entity/claim through a developmental framework, carrying altitude/state/quadrant/line + attribution. See core §4. |
| **Altitude** | A shared cross-framework developmental stage key (archaic, magic, mythic, rational, pluralistic, integral, …) used to align different frameworks. |
| **State × Stage** | The Wilber–Combs distinction: a state of consciousness (gross/subtle/causal/nondual) is interpreted through a developmental stage; the two are modeled separately. |
| **KID** | Canonical Kosmographica ID (e.g. `kg:entity/<uuid>`); the join target across source systems. |
| **`sameAs` / reconciliation** | The mapping that links a source-system record (or external authority ID) to a canonical KID. |
| **Source system** | An upstream dataset (Mythographica, Sacred-Lineage, Kosmotheon, time-thread) feeding the core. |
| **Federation** | Integrating source systems into the core without re-keying them. |
| **GraphRAG** | Retrieval that augments dense/sparse search with graph traversal over relationship/claim/comparative/developmental edges. |
| **Mythographica** | The comparative mythology graph (repo: Interpretatio-Universalis); source of the assertion model and comparative vocabulary. |
| **Sacred-Lineage / Kechimyaku** | The lineage-transmission dataset/app (guru–disciple chains). |
| **Kosmotheon** | The integral-developmental knowledge base (AQAL, Spiral Dynamics, Gebser, Wilber–Combs). |
| **time-thread** | The historical timeline spine. |
| **TK Labels / CARE** | Traditional Knowledge Labels and the CARE principles governing indigenous/sensitive content. |

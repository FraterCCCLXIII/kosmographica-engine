# Domain Module Authoring Guide

> **Status:** stub / outline · **Priority:** P0 · Part of the [spec plan](../PLAN.md).
> The template + rules for writing a domain module that conforms to the
> [core meta-model](../core-meta-model.md). The Religion & Mythology module is the reference example.

## Purpose

Ensure every domain module (Philosophy & Science, Art & Culture, Polity & Society, Technology, …)
extends the universal core consistently — same claim model, same cross-cutting layers, different
entity-subtype vocabulary.

## What a module may and may not do

- **May:** define its own `EntityType` subtypes, module-specific relationship/claim types, and
  module-specific entity-page sections.
- **May not:** redefine core fields, invent a parallel claim/confidence model, or bypass the
  federation, developmental, temporal, or provenance layers.

## Required sections (module template)

1. **Conformance preamble** — declares the module, links to the core, states "core governs on conflict."
2. **Scope & vision** — what this domain covers and its boundary with adjacent modules.
3. **Entity ontology** — the module's entity types/subtypes (a profile of core `Entity`).
4. **Module relationship & claim types** — additions to the controlled vocabulary (registered per
   [../governance/controlled-vocabulary.md](../governance/controlled-vocabulary.md)).
5. **Information architecture** — navigation + entity-page sections.
6. **Developmental layer usage** — how core §4 applies in this domain.
7. **Federation & source systems** — which datasets feed this module.
8. **Examples** — worked entity + claim examples.

## Conventions

- Confidence is numeric (0–1) + derived band (core §3.2).
- Every contestable assertion is a claim with sources.
- Cross-link to core sections rather than restating schema.

## Checklist before a module is "specified"

- [ ] Conforms to core entity/claim/relationship model.
- [ ] Entity types + vocabulary additions registered.
- [ ] Federation sources identified.
- [ ] Developmental + temporal usage stated.
- [ ] Reviewed against this guide.

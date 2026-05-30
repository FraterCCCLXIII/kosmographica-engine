# Licensing & Data Rights

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the licensing posture of the Kosmographica corpus and code, how source-dataset licenses
propagate, and how third-party media rights are tracked.

## Proposed posture (v1) — owner sign-off required

> Licensing is a **user-owned legal/business decision**. The below is a recommended default to
> unblock building; confirm or override before public launch.

### Per-record licensing, not one blanket license

Each record carries a `license` field. A single blanket corpus license can't work because upstream
sources differ (notably **Kosmotheon is CC-BY-SA**, whose share-alike obligation propagates to
derived content). Per-record licensing lets incompatible material coexist and be filtered on export.

| Layer | Recommended default | Why |
| --- | --- | --- |
| **Engine code** | AGPL-3.0 (or MIT if permissive reuse is preferred) | network-copyleft keeps a hosted graph open; MIT if adoption matters more |
| **Original corpus content** | CC-BY-SA-4.0 | compatible with Kosmotheon upstream; keeps the commons open |
| **Imported records** | inherit source license (stamped at ingestion) | legal correctness; no license laundering |
| **Media/images** | per-item `license` (`CC0 / CC-BY / … / rights_reserved`) + IIIF rights statement | image rights vary per object |

### Source-license propagation

The ingestion envelope carries `meta.license`; every imported record stamps its **source license**.
Records whose license is incompatible with redistribution are **segregated** (gated from bulk/open
export), not relicensed. Export honors per-record license filters.

### Attribution

Exports credit upstream sources and contributors (CC-BY/SA attribution chains preserved). Community
attribution for traditional knowledge is handled additionally via CARE/TK (below).

### Relationship to sovereignty

**TK Labels are not licenses** — a CC license governs copyright; a TK Label governs cultural
authority. They coexist: a record may be CC-BY *and* carry TK Secret/Sacred, in which case the
sovereignty gate ([ethics-and-sovereignty.md](./ethics-and-sovereignty.md)) overrides open access
regardless of the license.

## Key decisions / open questions

- [x] Single vs. per-record licensing → **per-record** (with source-license inheritance).
- [ ] **(user-owned)** Confirm engine code license (AGPL vs. MIT) and corpus license (CC-BY-SA).

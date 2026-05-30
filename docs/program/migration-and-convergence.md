# Migration & Convergence Plan

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define how the four existing repositories converge into the Kosmographica engine — in what order,
with what parity checks — without disrupting the apps that already work.

## Decided method (v1)

**Incremental, one source at a time** — never big-bang. Each source converges via its adapter
(emit envelope → pipeline), is parity-checked, and only then is the next source added. Source apps
**stay live** during convergence (read-through), with deprecation decided per app *after* parity holds.

### Convergence order (easiest/most-aligned first)

| # | Source | Why this order | Maps to |
| --- | --- | --- | --- |
| a | **Core + federation engine** | nothing ingests without it | — |
| b | **Mythographica** | already claim-shaped (nodes/edges + numeric confidence) → lowest-friction | nodes→entities, edges→relationships+claims |
| c | **Sacred-Lineage** | rich entities + lineage transmission; tests relationship modeling | Figure/Concept/Text/Practice→entities, Transmission/EntityLink→relationships+claims |
| d | **time-thread** | supplies the canonical chronology spine | timeline→events + Era/Period entities |
| e | **Kosmotheon** | prose → structured developmental layer; hardest extraction, do last | frameworks/stages→developmental annotations (depends on ADR-004) |

### Parity & validation before cutover

Each source ingestion is followed by a **parity check** (Sacred-Lineage `db:parity` precedent):
row/coverage counts source-vs-core, plus a reconciliation review of proposed `sameAs` links. A source
is "converged" only when parity passes and the review queue is cleared.

### Re-runnability

Imports are **idempotent** on `(source_system, external_id)` (ADR-010 / source-adapter skill), so any
source can be re-ingested safely; rollback = re-run from the source of truth. No destructive cutover.

## Key decisions / open questions

- [x] Big-bang vs. incremental → **incremental, parity-gated, one source at a time**.
- [ ] Fate of each source app post-convergence (live read-through vs. deprecate) — decide per app after parity.

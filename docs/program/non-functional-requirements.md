# Non-Functional Requirements

> **Status:** stub / outline · **Priority:** P2 · Part of the [spec plan](../PLAN.md).

## Purpose

Capture the quality attributes the system must meet — scale, performance, availability, and
operability — to size the architecture appropriately.

## Sections to detail

1. **Scale targets** — expected entity/claim/relationship counts; media volume; growth trajectory.
2. **Performance** — read latency budgets (entity page, graph traversal, RAG query); write/ingestion
   throughput.
3. **Availability & reliability** — uptime target, degradation modes, backup/restore, disaster recovery.
4. **Operability** — observability (logs, metrics, traces), audit trails, runbooks.
5. **Cost** — storage/compute envelope for the polystore; embedding/LLM cost model.
6. **Portability** — deployment targets (Docker/Coolify precedent in Sacred-Lineage).

## Key decisions / open questions

- [ ] Initial scale assumptions (tens of thousands vs. millions of entities).

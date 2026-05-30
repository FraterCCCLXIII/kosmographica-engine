---
name: kosmographica-adr
description: Append an Architecture Decision Record to the Kosmographica decision log in the repo's exact format, or supersede a prior decision. Use when recording a decision, writing an ADR, or changing an architectural choice in docs/governance/decision-log.md.
---

# Kosmographica ADR

Record significant decisions in `docs/governance/decision-log.md`. The log is **append-only**:
supersede rather than edit past decisions.

## Procedure

1. Read `docs/governance/decision-log.md`; find the highest `ADR-NNN` and the `## Still open` section.
2. Write the new record with the next number, placed **immediately before `## Still open`** (after the
   last accepted ADR, before the closing `---`).
3. If it replaces an earlier decision:
   - Set the old ADR's `Status:` to `superseded by ADR-NNN` (with a one-line note of what changed).
   - The new ADR's `Status:` is `accepted (supersedes ADR-MMM)`.
   - Do **not** delete the old record.
4. Keep it concise — this is a log, not an essay. Cross-link the spec doc the decision governs.

## Format

```text
## ADR-NNN: <imperative title>

- **Date:** YYYY-MM-DD
- **Status:** proposed | accepted | accepted (supersedes ADR-MMM) | superseded by ADR-MMM
- **Context:** why this decision is needed.
- **Options:** the alternatives weighed (omit if obvious).
- **Decision:** the choice, stated plainly.
- **Consequences:** the trade-off accepted — including the cost, not just the upside.
```

## Conventions

- Favor the **lean** option and say what is **deferred until forced** (the project's guiding principle).
- A decision that adds a service/dependency must state the trigger that justified it.
- After editing, the only expected lint output is proper-noun spellcheck noise — do not "fix" it.

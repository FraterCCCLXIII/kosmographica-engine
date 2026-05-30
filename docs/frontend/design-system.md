# Design System

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the design tokens and component library for Kosmographica's UI — fully themeable, accessible,
and consistent across all views (graph explorer, entity pages, comparison, developmental lens).

## Decided method (v1)

**Tailwind + shadcn/ui, driven entirely by design tokens as CSS variables.** shadcn (used in
time-thread) gives accessible, ownable primitives; Tailwind (used in Sacred-Lineage) maps utilities to
the token variables. **No hardcoded color/spacing/type values** — everything references a token.

### Tokens (single source of truth)

Tokens are CSS custom properties on `:root`, themed by data-attribute (`[data-theme]`):

- **color** — semantic roles (`--color-canvas`, `--color-surface`, `--color-ink`, `--color-accent`,
  `--color-muted`, `--color-border`, plus state colors). Adapt Sacred-Lineage's **warm-canvas** base
  (cream canvas, restrained accent).
- **typography** — serif display + humanist sans scale (`--font-display`, `--font-sans`, size/line
  steps).
- **spacing / radius / elevation** — stepped scales as tokens.

Light/dark and future custom themes are just alternate token sets; components never change.

### Component inventory

shadcn primitives + project-standard wrappers: `<Button>`, `<Input>`, `<Card>`, **`<Modal>`**,
**`<Dropdown>`**, `<Badge>`, `<Tabs>`, `<Nav>`, `<Table>`. Interactive elements are wrapped in the
standardized containers (per project UI conventions) for consistency + a11y.

### Knowledge-graph–specific tokens

- **Trust/confidence badges** — token-driven styles for the tier labels (`machine_validated`,
  `human_reviewed`, `expert_endorsed`) and a numeric confidence indicator (ADR-013). These appear on
  every entity/claim surface.
- **Graph legend** — node color by `type`, edge style by relationship/comparative/developmental class.
- **Altitude color scale** — a dedicated token ramp for the Developmental Lens (depends on ADR-003;
  define as `--altitude-*` tokens so the scale can be swapped when ADR-003 resolves).
- **TK / sensitivity badges** — token-driven badge styles for TK Labels + `sensitive/sacred/restricted`.

### Accessibility (default, not optional)

ARIA roles, full keyboard nav, visible focus states, WCAG-AA contrast enforced via tokens, responsive
by default. These are acceptance criteria for every component.

## Existing assets to adopt

- Sacred-Lineage `DESIGN.md` (warm-canvas token system, components, do/don'ts, responsive rules).

## Key decisions / open questions

- [x] Framework → **Tailwind + shadcn/ui**, tokens as CSS variables.
- [ ] Canonical altitude color scale for the developmental lens (ADR-003).

# Design System

> **Status:** stub / outline · **Priority:** P1 · Part of the [spec plan](../PLAN.md).

## Purpose

Define the design tokens and component library for Kosmographica's UI — fully themeable, accessible,
and consistent across all views (graph explorer, entity pages, comparison, developmental lens).

## Sections to detail

1. **Design tokens** — color, typography, spacing, radius, elevation as named tokens (no hardcoded
   values); light/dark + future custom themes.
2. **Base theme** — adopt/adapt Sacred-Lineage's warm-canvas token system (`DESIGN.md`): cream
   canvas, serif display + humanist sans, restrained accent.
3. **Component inventory** — buttons, inputs, cards, modals, dropdowns, badges, tabs, nav, tables;
   standardized containers (`<Modal>`, `<Dropdown>`) per project UI conventions.
4. **Graph/visualization styling** — node/edge legends by type + confidence; comparative edge colors;
   developmental altitude color scale (ties to core §10 Q3).
5. **Accessibility** — ARIA, keyboard nav, contrast, focus states, responsive by default.
6. **Theming architecture** — token source of truth, CSS variables, dark mode, theme switching.
7. **Iconography** — symbol/iconographic display conventions (sacred symbols, TK-label badges).

## Existing assets to adopt

- Sacred-Lineage `DESIGN.md` (token system, components, do/don'ts, responsive rules).

## Key decisions / open questions

- [ ] Component framework (shadcn/ui is used in time-thread; Sacred-Lineage is Tailwind).
- [ ] Canonical altitude color scale for the developmental lens.

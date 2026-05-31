/** Entity types that can show the transmission lineage viewer. */
export const LINEAGE_VIEW_TYPES = ["LineageChart", "School", "Tradition"] as const;

export type LineageViewType = (typeof LINEAGE_VIEW_TYPES)[number];

export function hasLineageView(type: string): type is LineageViewType {
  return (LINEAGE_VIEW_TYPES as readonly string[]).includes(type);
}

export type LineageViewMode = "horizontal" | "vertical" | "list";

export const LINEAGE_VIEW_MODE_KEY = "kg-lineage-view-mode";

export const LINEAGE_ZOOM_MIN = 0.35;
export const LINEAGE_ZOOM_MAX = 2.5;
export const LINEAGE_ZOOM_STEP = 0.15;
export const LINEAGE_ZOOM_DEFAULT = 1;

export function clampLineageZoom(value: number): number {
  return Math.min(LINEAGE_ZOOM_MAX, Math.max(LINEAGE_ZOOM_MIN, value));
}

export function readLineageViewMode(): LineageViewMode {
  if (typeof window === "undefined") return "horizontal";
  const stored = window.localStorage.getItem(LINEAGE_VIEW_MODE_KEY);
  if (stored === "horizontal" || stored === "vertical" || stored === "list") return stored;
  return "horizontal";
}

import type { EntityOut } from "@/lib/types";
import { fmtYear } from "@/lib/format";

export type CosmographEra = {
  id: string;
  label: string;
  /** Inclusive lower bound; null = no lower bound. */
  from: number | null;
  /** Exclusive upper bound; null = no upper bound. */
  to: number | null;
};

export const COSMOGRAPH_ERAS: CosmographEra[] = [
  { id: "prehistory", label: "Prehistory & deep antiquity", from: null, to: -3000 },
  { id: "ancient", label: "Ancient & classical", from: -3000, to: 500 },
  { id: "medieval", label: "Medieval & late antique", from: 500, to: 1500 },
  { id: "early-modern", label: "Early modern", from: 1500, to: 1800 },
  { id: "modern", label: "Modern", from: 1800, to: 1950 },
  { id: "contemporary", label: "Contemporary", from: 1950, to: null },
];

export type TimelineEntry = {
  entity: EntityOut;
  yearLabel: string;
  sortKey: number;
  eraId: string;
};

export type TimelineEraGroup = {
  era: CosmographEra;
  entries: TimelineEntry[];
};

function eraForYear(year: number | null): CosmographEra {
  if (year === null) {
    return { id: "undated", label: "Undated & prehistoric", from: null, to: null };
  }
  for (const era of COSMOGRAPH_ERAS) {
    const above = era.from === null || year >= era.from;
    const below = era.to === null || year < era.to;
    if (above && below) return era;
  }
  return COSMOGRAPH_ERAS[COSMOGRAPH_ERAS.length - 1];
}

function yearLabel(entity: EntityOut): string {
  const dataRange =
    typeof entity.data.date_range === "string" ? entity.data.date_range.trim() : "";
  if (dataRange) return dataRange;
  const from = fmtYear(entity.valid_from);
  const to = fmtYear(entity.valid_to);
  if (from && to) return `${from} – ${to}`;
  return from ?? to ?? "Date unknown";
}

function sortKey(entity: EntityOut): number {
  if (entity.valid_from !== null) return entity.valid_from;
  // Undated entries sink to the bottom of their era bucket.
  return Number.POSITIVE_INFINITY;
}

export function buildCosmographTimeline(entities: EntityOut[]): TimelineEraGroup[] {
  const entries: TimelineEntry[] = entities.map((entity) => {
    const era = eraForYear(entity.valid_from);
    return {
      entity,
      yearLabel: yearLabel(entity),
      sortKey: sortKey(entity),
      eraId: era.id,
    };
  });

  const byEra = new Map<string, TimelineEntry[]>();
  for (const entry of entries) {
    const list = byEra.get(entry.eraId) ?? [];
    list.push(entry);
    byEra.set(entry.eraId, list);
  }

  const eraOrder = [...COSMOGRAPH_ERAS.map((e) => e.id), "undated"];
  const groups: TimelineEraGroup[] = [];

  for (const eraId of eraOrder) {
    const bucket = byEra.get(eraId);
    if (!bucket?.length) continue;
    bucket.sort((a, b) => a.sortKey - b.sortKey || a.entity.label.localeCompare(b.entity.label));
    const era =
      eraId === "undated"
        ? { id: "undated", label: "Undated & prehistoric", from: null, to: null }
        : COSMOGRAPH_ERAS.find((e) => e.id === eraId)!;
    groups.push({ era, entries: bucket });
  }

  return groups;
}

export function cosmographFacet(
  entity: EntityOut,
  key: string,
): string | null {
  const value = entity.data[key];
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

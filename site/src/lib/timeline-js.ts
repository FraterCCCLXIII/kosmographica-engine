import type { TimelineEraGroup } from "@/lib/cosmograph-timeline";
import { cosmographFacet } from "@/lib/cosmograph-timeline";
import { entityImage } from "@/lib/entity-media";
import { entityHref } from "@/lib/types";
import type { EntityOut } from "@/lib/types";

/** Subset of the TimelineJS JSON schema — https://timeline.knightlab.com/docs/json-format.html */
export type TimelineJsDate = {
  year: number;
  month?: number;
  day?: number;
  display_date?: string;
};

export type TimelineJsText = {
  headline?: string;
  text?: string;
};

export type TimelineJsMedia = {
  url: string;
  caption?: string;
  credit?: string;
  thumbnail?: string;
  alt?: string;
  link?: string;
};

export type TimelineJsEvent = {
  start_date: TimelineJsDate;
  end_date?: TimelineJsDate;
  text?: TimelineJsText;
  media?: TimelineJsMedia;
  group?: string;
  display_date?: string;
  unique_id?: string;
  autolink?: boolean;
};

export type TimelineJsEra = {
  start_date: TimelineJsDate;
  end_date: TimelineJsDate;
  text?: TimelineJsText;
};

export type TimelineJsData = {
  events: TimelineJsEvent[];
  title?: TimelineJsEvent;
  eras?: TimelineJsEra[];
  /** Required for dates before ~271,821 BCE and cosmograph deep prehistory. */
  scale?: "human" | "cosmological";
};

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function facetLine(entity: EntityOut): string {
  const parts = [
    cosmographFacet(entity, "tradition"),
    cosmographFacet(entity, "cosmograph_type"),
    cosmographFacet(entity, "domain"),
    cosmographFacet(entity, "topology"),
  ].filter(Boolean);
  return parts.join(" · ");
}

function slideBody(entity: EntityOut): string {
  const description =
    typeof entity.data.description === "string" ? entity.data.description.trim() : "";
  const importance =
    typeof entity.data.importance === "string" ? entity.data.importance.trim() : "";
  const sources = cosmographFacet(entity, "primary_sources");
  const human = cosmographFacet(entity, "human_position");
  const path = cosmographFacet(entity, "liberation_path");
  const href = entityHref(entity);

  const chunks: string[] = [];
  if (description) chunks.push(`<p>${escapeHtml(description)}</p>`);
  if (importance && importance !== description) {
    chunks.push(`<p><em>${escapeHtml(importance)}</em></p>`);
  }
  const meta: string[] = [];
  if (human) meta.push(`Human position: ${escapeHtml(human)}`);
  if (path) meta.push(`Liberation path: ${escapeHtml(path)}`);
  if (sources) meta.push(`Sources: ${escapeHtml(sources)}`);
  if (meta.length) chunks.push(`<p>${meta.join("<br>")}</p>`);
  chunks.push(
    `<p><a href="${escapeHtml(href)}">Open full record in Kosmographica →</a></p>`,
  );
  return chunks.join("");
}

function startDate(entity: EntityOut, display: string): TimelineJsDate {
  if (entity.valid_from !== null) {
    return {
      year: entity.valid_from,
      display_date: display,
    };
  }
  const lower = display.toLowerCase();
  if (lower.includes("prehistoric") || lower.includes("bce+")) {
    return { year: -20000, display_date: display };
  }
  if (lower.includes("global")) {
    return { year: 1950, display_date: display };
  }
  return { year: 1800, display_date: display || "Date unknown" };
}

function eventFromEntry(
  entry: TimelineEraGroup["entries"][number],
  group: string,
): TimelineJsEvent {
  const { entity, yearLabel } = entry;
  const image = entityImage(entity);
  const href = entityHref(entity);

  const slide: TimelineJsEvent = {
    unique_id: entity.slug,
    group,
    display_date: yearLabel,
    start_date: startDate(entity, yearLabel),
    text: {
      headline: `<a href="${escapeHtml(href)}">${escapeHtml(entity.label)}</a>`,
      text: slideBody(entity),
    },
    autolink: false,
  };

  if (image?.imageUrl) {
    slide.media = {
      url: image.imageUrl,
      thumbnail: image.thumbnailUrl,
      alt: image.title ?? entity.label,
      caption: facetLine(entity) || undefined,
      credit: [image.source, image.license].filter(Boolean).join(" · ") || undefined,
      link: image.pageUrl ?? href,
    };
  }

  return slide;
}

function eraToTimelineJs(era: TimelineEraGroup["era"]): TimelineJsEra | null {
  if (era.id === "undated") return null;
  const startYear = era.from ?? -500000;
  const endYear = era.to ?? 2100;
  return {
    start_date: { year: startYear },
    end_date: { year: endYear },
    text: { headline: era.label },
  };
}

/** Convert grouped cosmograph entries into TimelineJS JSON (Knight Lab). */
export function cosmographsToTimelineJs(groups: TimelineEraGroup[]): TimelineJsData {
  const events: TimelineJsEvent[] = [];

  for (const group of groups) {
    for (const entry of group.entries) {
      events.push(eventFromEntry(entry, group.era.label));
    }
  }

  events.sort(
    (a, b) =>
      a.start_date.year - b.start_date.year ||
      (a.text?.headline ?? "").localeCompare(b.text?.headline ?? ""),
  );

  const eras = groups
    .map((g) => eraToTimelineJs(g.era))
    .filter((e): e is TimelineJsEra => e !== null);

  return {
    scale: "cosmological",
    title: {
      start_date: { year: -50000 },
      text: {
        headline: "Cosmographs — maps of reality",
        text: "<p>A chronological catalog of humanity's cosmographs: mythic, metaphysical, scientific, psychological, and informational maps of cosmos, mind, and knowledge.</p><p>Scroll the timeline below or click any marker to read an entry. Built with <a href='https://timeline.knightlab.com/' target='_blank' rel='noopener noreferrer'>Timeline JS</a> by Northwestern Knight Lab.</p>",
      },
    },
    eras,
    events,
  };
}

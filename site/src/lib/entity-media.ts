import type { EntityOut } from "@/lib/types";

export type EntityImage = {
  /** Best URL for cards, timeline markers, and inline display. */
  thumbnailUrl: string;
  /** Full-size when raster; otherwise same as thumbnailUrl. */
  imageUrl: string;
  title?: string;
  source?: string;
  license?: string;
  pageUrl?: string;
};

const RASTER_RE = /\.(jpg|jpeg|png|gif|webp|svg)(\?|#|$)|\/thumb\//i;
const NON_RASTER_RE = /\.(pdf|djvu|tiff?|doc|docx)(\?|#|$)/i;

export function isDisplayableImageUrl(url: string): boolean {
  const trimmed = url.trim();
  if (!trimmed) return false;
  if (NON_RASTER_RE.test(trimmed)) return false;
  return RASTER_RE.test(trimmed);
}

function resolveImageUrls(thumbnailUrl: string, imageUrl: string): { display: string; full: string } | null {
  const thumb = thumbnailUrl.trim();
  const full = imageUrl.trim();
  if (!thumb && !full) return null;

  const display =
    [thumb, full].find(isDisplayableImageUrl) ?? thumb ?? full;
  const bestFull = isDisplayableImageUrl(full) ? full : display;
  return { display, full: bestFull };
}

export function entityImage(entity: EntityOut): EntityImage | null {
  const d = entity.data;
  const thumbnailUrl =
    typeof d.thumbnail_url === "string" ? d.thumbnail_url.trim() : "";
  const imageUrl = typeof d.image_url === "string" ? d.image_url.trim() : "";
  const resolved = resolveImageUrls(thumbnailUrl, imageUrl);
  if (!resolved) return null;

  return {
    thumbnailUrl: resolved.display,
    imageUrl: resolved.full,
    title: typeof d.image_title === "string" ? d.image_title : undefined,
    source: typeof d.image_source === "string" ? d.image_source : undefined,
    license: typeof d.image_license === "string" ? d.image_license : undefined,
    pageUrl: typeof d.image_page_url === "string" ? d.image_page_url : undefined,
  };
}

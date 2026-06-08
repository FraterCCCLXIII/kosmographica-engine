import type { EntityOut } from "@/lib/types";

export type EntityImage = {
  thumbnailUrl: string;
  imageUrl: string;
  title?: string;
  source?: string;
  license?: string;
  pageUrl?: string;
};

export function entityImage(entity: EntityOut): EntityImage | null {
  const d = entity.data;
  const thumbnailUrl =
    typeof d.thumbnail_url === "string" ? d.thumbnail_url.trim() : "";
  const imageUrl = typeof d.image_url === "string" ? d.image_url.trim() : "";
  if (!thumbnailUrl && !imageUrl) return null;
  return {
    thumbnailUrl: thumbnailUrl || imageUrl,
    imageUrl: imageUrl || thumbnailUrl,
    title: typeof d.image_title === "string" ? d.image_title : undefined,
    source: typeof d.image_source === "string" ? d.image_source : undefined,
    license: typeof d.image_license === "string" ? d.image_license : undefined,
    pageUrl: typeof d.image_page_url === "string" ? d.image_page_url : undefined,
  };
}

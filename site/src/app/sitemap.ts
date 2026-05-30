import type { MetadataRoute } from "next";
import { api } from "@/lib/api";
import { entityHref } from "@/lib/types";

const SITE_URL = process.env.SITE_URL ?? "http://localhost:3099";

export const revalidate = 3600;

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const base: MetadataRoute.Sitemap = [
    { url: SITE_URL, changeFrequency: "daily", priority: 1 },
    { url: `${SITE_URL}/search`, changeFrequency: "weekly", priority: 0.5 },
  ];
  try {
    const page = await api.listEntities({ limit: 200 });
    return base.concat(
      page.items.map((e) => ({
        url: SITE_URL + entityHref(e),
        changeFrequency: "weekly" as const,
        priority: 0.7,
      })),
    );
  } catch {
    return base;
  }
}

import { api, ApiError } from "@/lib/api";

/** URL slug → engine entity `type` value. */
export const BROWSE_GROUPS = [
  {
    id: "divine",
    label: "Divine beings",
    types: [
      {
        slug: "deity",
        apiType: "Deity",
        label: "Deity",
        labelPlural: "Deities",
        description: "Gods, goddesses, and divine figures across traditions.",
      },
      {
        slug: "primordial",
        apiType: "Primordial",
        label: "Primordial",
        labelPlural: "Primordials",
        description: "Cosmic origins, first beings, and foundational powers.",
      },
      {
        slug: "demon",
        apiType: "Demon",
        label: "Demon",
        labelPlural: "Demons",
        description: "Malevolent or liminal supernatural beings.",
      },
    ],
  },
  {
    id: "people",
    label: "People",
    types: [
      {
        slug: "figure",
        apiType: "Figure",
        label: "Figure",
        labelPlural: "Figures",
        description: "Masters, teachers, saints, and historical spiritual figures.",
      },
      {
        slug: "hero",
        apiType: "Hero",
        label: "Hero",
        labelPlural: "Heroes",
        description: "Mythic heroes and legendary champions.",
      },
      {
        slug: "sage",
        apiType: "Sage",
        label: "Sage",
        labelPlural: "Sages",
        description: "Wisdom figures, philosophers, and seers.",
      },
    ],
  },
  {
    id: "traditions",
    label: "Traditions & schools",
    types: [
      {
        slug: "tradition",
        apiType: "Tradition",
        label: "Tradition",
        labelPlural: "Traditions",
        description: "Religious and spiritual traditions.",
      },
      {
        slug: "school",
        apiType: "School",
        label: "School",
        labelPlural: "Schools",
        description: "Schools, sects, and lineages within traditions.",
      },
      {
        slug: "lineage-chart",
        apiType: "LineageChart",
        label: "Lineage chart",
        labelPlural: "Lineage charts",
        description: "Transmission charts and succession maps.",
      },
    ],
  },
  {
    id: "cosmographs",
    label: "Maps of reality",
    types: [
      {
        slug: "cosmograph",
        apiType: "Cosmograph",
        label: "Cosmograph",
        labelPlural: "Cosmographs",
        description:
          "Cosmographs — mythic, metaphysical, scientific, and informational maps of reality.",
      },
    ],
  },
  {
    id: "ideas",
    label: "Ideas & texts",
    types: [
      {
        slug: "concept",
        apiType: "Concept",
        label: "Concept",
        labelPlural: "Concepts",
        description: "Doctrines, ideas, and abstract personifications.",
      },
      {
        slug: "motif",
        apiType: "Motif",
        label: "Motif",
        labelPlural: "Motifs",
        description: "Recurring mythic patterns and themes.",
      },
      {
        slug: "text",
        apiType: "Text",
        label: "Text",
        labelPlural: "Texts",
        description: "Scriptures, commentaries, and sacred writings.",
      },
    ],
  },
] as const satisfies ReadonlyArray<{
  id: string;
  label: string;
  types: ReadonlyArray<{
    slug: string;
    apiType: string;
    label: string;
    labelPlural: string;
    description: string;
  }>;
}>;

export type BrowseTypeDef = {
  slug: string;
  apiType: string;
  label: string;
  labelPlural: string;
  description: string;
};

export type BrowseTypeWithCount = BrowseTypeDef & { count: number };

export type BrowseGroupWithCounts = {
  id: string;
  label: string;
  types: BrowseTypeWithCount[];
};

export type BrowseCatalog = {
  groups: BrowseGroupWithCounts[];
  total: number;
};

export const BROWSE_PAGE_SIZE = 200;

export function allBrowseTypes(): BrowseTypeDef[] {
  return BROWSE_GROUPS.flatMap((g) => g.types.map((t) => ({ ...t })));
}

const SLUG_INDEX = new Map<string, BrowseTypeDef>(
  allBrowseTypes().map((t) => [t.slug, t]),
);

const API_TYPE_INDEX = new Map<string, BrowseTypeDef>(
  allBrowseTypes().map((t) => [t.apiType, t]),
);

export function getBrowseType(slug: string): BrowseTypeDef | undefined {
  return SLUG_INDEX.get(slug);
}

export function apiTypeToSlug(apiType: string): string | undefined {
  return API_TYPE_INDEX.get(apiType)?.slug;
}

export function browseHref(slug: string, page = 1): string {
  return page <= 1 ? `/browse/${slug}` : `/browse/${slug}?page=${page}`;
}

export async function fetchBrowseCatalog(): Promise<BrowseCatalog> {
  const counts = await Promise.all(
    allBrowseTypes().map(async (t) => {
      try {
        const page = await api.listEntities({ type: t.apiType, limit: 1 });
        return { slug: t.slug, count: page.total };
      } catch {
        return { slug: t.slug, count: 0 };
      }
    }),
  );
  const countBySlug = new Map(counts.map((c) => [c.slug, c.count]));

  const groups: BrowseGroupWithCounts[] = BROWSE_GROUPS.map((g) => ({
    id: g.id,
    label: g.label,
    types: g.types.map((t) => ({ ...t, count: countBySlug.get(t.slug) ?? 0 })),
  }));

  return {
    groups,
    total: counts.reduce((sum, c) => sum + c.count, 0),
  };
}

/** Empty catalog when the engine is offline (nav still renders). */
export function emptyBrowseCatalog(): BrowseCatalog {
  return {
    groups: BROWSE_GROUPS.map((g) => ({
      id: g.id,
      label: g.label,
      types: g.types.map((t) => ({ ...t, count: 0 })),
    })),
    total: 0,
  };
}

export async function loadBrowseCatalog(): Promise<BrowseCatalog> {
  try {
    return await fetchBrowseCatalog();
  } catch (e) {
    if (e instanceof ApiError) return emptyBrowseCatalog();
    throw e;
  }
}

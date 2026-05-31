import type { TrustTier } from "./types";

export const TIER_META: Record<TrustTier, { label: string; cls: string; title: string }> = {
  machine_unverified: {
    label: "Unverified",
    cls: "border-tier-unverified text-tier-unverified",
    title: "AI-authored, not yet verified — normally hidden from the public view.",
  },
  machine_validated: {
    label: "AI-verified",
    cls: "border-tier-validated text-tier-validated",
    title: "Verified by an automated checker against its cited source (publish-then-verify).",
  },
  human_reviewed: {
    label: "Human-reviewed",
    cls: "border-tier-reviewed text-tier-reviewed",
    title: "Reviewed and promoted by a human editor.",
  },
  expert_endorsed: {
    label: "Expert-endorsed",
    cls: "border-tier-expert text-tier-expert",
    title: "Endorsed by a domain expert.",
  },
};

// Historicity facet (engine: data.status, derived by kge.taxonomy). Orthogonal to type.
export const STATUS_META: Record<
  string,
  { label: string; title: string }
> = {
  historical: {
    label: "Historical",
    title: "Attested as a historical person (e.g. a documented master or teacher).",
  },
  legendary: {
    label: "Legendary",
    title: "A legendary or quasi-historical figure (heroes, mythic kings).",
  },
  mythic: {
    label: "Mythic",
    title: "A mythic being — divine, primordial, or demonic — not a historical person.",
  },
  reconstructed: {
    label: "Reconstructed",
    title: "Scholarly reconstruction (e.g. a Proto-Indo-European deity), not directly attested.",
  },
  unknown: {
    label: "Historicity unknown",
    title: "Historicity is undetermined from the source.",
  },
};

export function pct(n: number): string {
  return `${Math.round(n * 100)}%`;
}

// A signed year -> "800 BCE" / "1100 CE".
export function fmtYear(year: number | null | undefined): string | null {
  if (year === null || year === undefined) return null;
  return year < 0 ? `${-year} BCE` : `${year} CE`;
}

export function lifespan(from: number | null, to: number | null): string | null {
  const a = fmtYear(from);
  const b = fmtYear(to);
  if (a && b) return `${a} – ${b}`;
  return a ?? b;
}

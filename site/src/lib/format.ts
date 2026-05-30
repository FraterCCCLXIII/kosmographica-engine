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

import type { TrustTier } from "./types";

export const TIER_META: Record<TrustTier, { label: string; cls: string }> = {
  machine_unverified: { label: "Unverified", cls: "border-tier-unverified text-tier-unverified" },
  machine_validated: { label: "AI-validated", cls: "border-tier-validated text-tier-validated" },
  human_reviewed: { label: "Human-reviewed", cls: "border-tier-reviewed text-tier-reviewed" },
  expert_endorsed: { label: "Expert-endorsed", cls: "border-tier-expert text-tier-expert" },
};

export function fmtDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export function pct(n: number): string {
  return `${Math.round(n * 100)}%`;
}

// A signed year -> "800 BCE" / "1100 CE".
export function fmtYear(year: number | null): string | null {
  if (year === null || year === undefined) return null;
  return year < 0 ? `${-year} BCE` : `${year} CE`;
}

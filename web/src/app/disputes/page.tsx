import { api } from "@/lib/api";
import { PageHeader, EmptyState } from "@/components/Card";
import { ClaimCard } from "@/components/ClaimCard";

export default async function DisputesPage() {
  const page = await api.disputes(100);
  return (
    <div>
      <PageHeader
        title="Disputes"
        subtitle="Contradicting claims coexist with provenance — no AI edit wars. Humans adjudicate."
      />
      <div className="space-y-3">
        {page.items.length === 0 ? (
          <EmptyState>No open disputes. 🎉</EmptyState>
        ) : (
          page.items.map((claim) => <ClaimCard key={claim.id} claim={claim} />)
        )}
      </div>
    </div>
  );
}

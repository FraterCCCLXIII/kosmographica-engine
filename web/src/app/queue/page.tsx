import { api } from "@/lib/api";
import { PageHeader, EmptyState } from "@/components/Card";
import { ClaimCard } from "@/components/ClaimCard";

export default async function QueuePage({
  searchParams,
}: {
  searchParams: Promise<{ generator?: string; batch_id?: string }>;
}) {
  const { generator, batch_id } = await searchParams;
  const page = await api.claims({
    tier: "machine_validated",
    generator,
    batch_id,
    limit: 100,
  });

  return (
    <div>
      <PageHeader
        title="AI-validated queue"
        subtitle={
          <>
            Claims the verifier promoted to <code className="font-mono">machine_validated</code> —
            public, but unreviewed by a human. {page.total.toLocaleString()} total.
          </>
        }
      />

      <form className="mb-6 flex flex-wrap gap-2">
        <input
          name="generator"
          defaultValue={generator}
          placeholder="generator (e.g. gpt-…)"
          className="rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />
        <input
          name="batch_id"
          defaultValue={batch_id}
          placeholder="batch id"
          className="rounded-lg border border-border bg-surface px-3 py-2 text-sm outline-none focus:border-accent"
        />
        <button className="rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-foreground/5">
          Filter
        </button>
      </form>

      <div className="space-y-3">
        {page.items.length === 0 ? (
          <EmptyState>Nothing in the queue for this filter.</EmptyState>
        ) : (
          page.items.map((claim) => <ClaimCard key={claim.id} claim={claim} />)
        )}
      </div>
    </div>
  );
}

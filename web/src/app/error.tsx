"use client";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="rounded-xl border border-disputed/40 bg-surface p-6">
      <h2 className="text-lg font-semibold text-disputed">Could not reach the engine</h2>
      <p className="mt-2 text-sm text-muted">
        The console is read-only and depends on the engine API. Make sure it is running
        (<code className="font-mono">uvicorn kge.api.app:app</code>) and that{" "}
        <code className="font-mono">KGE_API_URL</code> points to it.
      </p>
      <pre className="mt-3 overflow-x-auto rounded-lg bg-foreground/5 p-3 text-xs text-muted">
        {error.message}
      </pre>
      <button
        onClick={reset}
        className="mt-4 rounded-lg border border-border px-3 py-1.5 text-sm font-medium hover:bg-foreground/5"
      >
        Retry
      </button>
    </div>
  );
}

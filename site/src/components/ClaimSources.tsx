import type { SourceOut, SupportSpan } from "@/lib/types";

export function ClaimSources({
  sources,
  spans,
}: {
  sources: SourceOut[];
  spans: SupportSpan[];
}) {
  if (sources.length === 0 && spans.length === 0) return null;
  return (
    <div className="mt-3 border-t border-border pt-3">
      {spans.length > 0 && (
        <ul className="space-y-1.5">
          {spans.map((s, i) => (
            <li key={i} className="border-l-2 border-border pl-3 text-sm italic text-muted">
              “{s.quote}”
            </li>
          ))}
        </ul>
      )}
      {sources.length > 0 && (
        <p className="mt-2 text-xs text-muted">
          <span className="font-medium">Sources: </span>
          {sources.map((src, i) => (
            <span key={src.id}>
              {i > 0 && "; "}
              {src.uri ? (
                <a
                  href={src.uri}
                  target="_blank"
                  rel="noreferrer"
                  className="text-accent-ink hover:underline"
                >
                  {src.citation}
                </a>
              ) : (
                src.citation
              )}
            </span>
          ))}
        </p>
      )}
    </div>
  );
}

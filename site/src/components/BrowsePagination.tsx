import Link from "next/link";
import { browseHref } from "@/lib/browse-catalog";

export function BrowsePagination({
  slug,
  page,
  total,
  pageSize,
}: {
  slug: string;
  page: number;
  total: number;
  pageSize: number;
}) {
  const pageCount = Math.max(1, Math.ceil(total / pageSize));
  if (pageCount <= 1) return null;

  const start = (page - 1) * pageSize + 1;
  const end = Math.min(page * pageSize, total);

  return (
    <nav
      aria-label="Pagination"
      className="mt-8 flex flex-wrap items-center justify-between gap-4 border-t border-border pt-5"
    >
      <p className="text-sm text-muted tabular-nums">
        Showing {start.toLocaleString()}–{end.toLocaleString()} of {total.toLocaleString()}
      </p>
      <div className="flex items-center gap-2">
        {page > 1 ? (
          <Link
            href={browseHref(slug, page - 1)}
            className="rounded-md border border-border px-3 py-1.5 text-sm transition-colors hover:border-accent hover:text-accent-ink"
          >
            Previous
          </Link>
        ) : (
          <span className="rounded-md border border-border px-3 py-1.5 text-sm text-muted">Previous</span>
        )}
        <span className="px-2 text-sm tabular-nums text-muted">
          {page} / {pageCount}
        </span>
        {page < pageCount ? (
          <Link
            href={browseHref(slug, page + 1)}
            className="rounded-md border border-border px-3 py-1.5 text-sm transition-colors hover:border-accent hover:text-accent-ink"
          >
            Next
          </Link>
        ) : (
          <span className="rounded-md border border-border px-3 py-1.5 text-sm text-muted">Next</span>
        )}
      </div>
    </nav>
  );
}

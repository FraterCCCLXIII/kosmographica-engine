import Link from "next/link";

export default function NotFound() {
  return (
    <div className="py-16 text-center">
      <h1 className="text-2xl font-semibold tracking-tight">Not found</h1>
      <p className="mt-2 text-sm text-muted">
        That entry doesn’t exist, or isn’t public.
      </p>
      <Link href="/" className="mt-4 inline-block text-sm text-accent-ink underline">
        Back to the encyclopedia
      </Link>
    </div>
  );
}

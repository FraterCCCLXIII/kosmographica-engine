import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { Nav } from "@/components/Nav";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Kosmographica — Audit Console",
  description: "Read-only audit console over the AI-populated claim graph.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full">
        <div className="mx-auto flex min-h-screen max-w-7xl">
          <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border bg-surface p-5 md:flex">
            <Link href="/" className="mb-1 text-lg font-semibold tracking-tight">
              Kosmographica
            </Link>
            <div className="mb-6 inline-flex w-fit items-center rounded-full border border-border px-2 py-0.5 text-xs text-muted">
              Audit Console · read-only
            </div>
            <Nav />
            <p className="mt-auto pt-6 text-xs leading-relaxed text-muted">
              AI is the only writer (publish-then-verify). Humans observe and audit.
            </p>
          </aside>
          <main className="min-w-0 flex-1 px-6 py-8">{children}</main>
        </div>
      </body>
    </html>
  );
}

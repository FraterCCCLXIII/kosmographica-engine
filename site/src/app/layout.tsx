import type { Metadata } from "next";
import { Spectral, Inter } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { SearchBox } from "@/components/SearchBox";

const display = Spectral({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});
const sans = Inter({ variable: "--font-sans", subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "Kosmographica — a graph of human thought",
    template: "%s · Kosmographica",
  },
  description:
    "A federated, source-grounded encyclopedia of religion, mythology, and human thought. Every claim is cited and trust-rated.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${sans.variable} h-full antialiased`}
    >
      <body className="min-h-full">
        <header className="sticky top-0 z-10 border-b border-border bg-canvas/85 backdrop-blur">
          <div className="mx-auto flex max-w-5xl items-center gap-4 px-5 py-3">
            <Link href="/" className="text-xl font-semibold tracking-tight">
              Kosmographica
            </Link>
            <span className="hidden text-sm text-muted sm:inline">a graph of human thought</span>
            <div className="ml-auto w-full max-w-xs">
              <SearchBox />
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-5 py-8">{children}</main>
        <footer className="mx-auto max-w-5xl px-5 py-10 text-xs leading-relaxed text-muted">
          Every claim shown is grounded in a cited source and carries a trust rating.
          Authored by AI under publish-then-verify; reviewed over time.
        </footer>
      </body>
    </html>
  );
}

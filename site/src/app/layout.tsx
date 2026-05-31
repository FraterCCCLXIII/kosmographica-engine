import type { Metadata } from "next";
import { Spectral, Inter } from "next/font/google";
import "./globals.css";
import { NavShell } from "@/components/NavShell";
import { loadBrowseCatalog } from "@/lib/browse-catalog";
import { themeBootScript } from "@/lib/theme";

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

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const browseCatalog = await loadBrowseCatalog();

  return (
    <html
      lang="en"
      className={`${display.variable} ${sans.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeBootScript }} />
      </head>
      <body className="h-full">
        <NavShell browseCatalog={browseCatalog}>{children}</NavShell>
      </body>
    </html>
  );
}

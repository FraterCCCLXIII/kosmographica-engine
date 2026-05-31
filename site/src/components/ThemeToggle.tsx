"use client";

import { useCallback, useSyncExternalStore } from "react";
import { readTheme, subscribeTheme, writeTheme, type Theme } from "@/lib/theme";

function readResolvedTheme(): Theme {
  return readTheme();
}

export function ThemeToggle() {
  const theme = useSyncExternalStore(subscribeTheme, readResolvedTheme, () => "light" as Theme);

  const toggle = useCallback(() => {
    writeTheme(theme === "dark" ? "light" : "dark");
  }, [theme]);

  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      title={isDark ? "Light mode" : "Dark mode"}
      className="inline-flex h-9 w-9 items-center justify-center rounded-md text-ink transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
    >
      {isDark ? (
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden fill="none">
          <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.75" />
          <path
            d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"
            stroke="currentColor"
            strokeWidth="1.75"
            strokeLinecap="round"
          />
        </svg>
      ) : (
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden fill="none">
          <path
            d="M21 14.5A7.5 7.5 0 0 1 9.5 3.2a7.5 7.5 0 1 0 11.5 11.3Z"
            stroke="currentColor"
            strokeWidth="1.75"
            strokeLinejoin="round"
          />
        </svg>
      )}
    </button>
  );
}

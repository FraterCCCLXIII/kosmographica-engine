export type Theme = "light" | "dark";

export const THEME_STORAGE_KEY = "kg-theme";
export const THEME_EVENT = "kg-theme-change";

export function readTheme(): Theme {
  const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (stored === "light" || stored === "dark") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function applyTheme(theme: Theme): void {
  document.documentElement.dataset.theme = theme;
}

export function writeTheme(theme: Theme): void {
  window.localStorage.setItem(THEME_STORAGE_KEY, theme);
  applyTheme(theme);
  window.dispatchEvent(new Event(THEME_EVENT));
}

export function subscribeTheme(callback: () => void): () => void {
  window.addEventListener(THEME_EVENT, callback);
  window.addEventListener("storage", callback);
  return () => {
    window.removeEventListener(THEME_EVENT, callback);
    window.removeEventListener("storage", callback);
  };
}

/** Inline boot script — run before paint to avoid theme flash. */
export const themeBootScript = `(function(){try{var t=localStorage.getItem("${THEME_STORAGE_KEY}");var d=t==="dark"||(!t&&window.matchMedia("(prefers-color-scheme: dark)").matches);document.documentElement.dataset.theme=d?"dark":"light";}catch(e){}})();`;

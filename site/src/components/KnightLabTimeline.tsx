"use client";

import { useEffect, useId, useRef } from "react";
import type { TimelineJsData } from "@/lib/timeline-js";

const TIMELINE_CSS =
  "https://cdn.knightlab.com/libs/timeline3/latest/css/timeline.css";
const TIMELINE_JS =
  "https://cdn.knightlab.com/libs/timeline3/latest/js/timeline.js";

type TimelineInstance = { destroy?: () => void };

declare global {
  interface Window {
    TL?: {
      Timeline: new (
        containerId: string,
        data: TimelineJsData,
        options?: Record<string, unknown>,
      ) => TimelineInstance;
    };
  }
}

function loadStylesheet(href: string): HTMLLinkElement {
  const existing = document.querySelector<HTMLLinkElement>(
    `link[href="${href}"]`,
  );
  if (existing) return existing;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  link.title = "timeline-styles";
  document.head.appendChild(link);
  return link;
}

function loadScript(src: string): Promise<void> {
  const existing = document.querySelector<HTMLScriptElement>(
    `script[src="${src}"]`,
  );
  if (existing?.dataset.loaded === "true") return Promise.resolve();
  if (existing) {
    return new Promise((resolve, reject) => {
      existing.addEventListener("load", () => resolve(), { once: true });
      existing.addEventListener("error", () => reject(new Error(src)), {
        once: true,
      });
    });
  }
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = () => {
      script.dataset.loaded = "true";
      resolve();
    };
    script.onerror = () => reject(new Error(`Failed to load ${src}`));
    document.body.appendChild(script);
  });
}

export function KnightLabTimeline({ data }: { data: TimelineJsData }) {
  const reactId = useId();
  const containerId = `timeline-${reactId.replace(/:/g, "")}`;
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<TimelineInstance | null>(null);
  const dataRef = useRef(data);
  dataRef.current = data;

  useEffect(() => {
    let cancelled = false;

    async function mount() {
      loadStylesheet(TIMELINE_CSS);
      await loadScript(TIMELINE_JS);
      if (cancelled || !containerRef.current || !window.TL) return;

      containerRef.current.innerHTML = "";
      timelineRef.current = new window.TL.Timeline(
        containerId,
        dataRef.current,
        {
          font: "georgia-helvetica",
          initial_zoom: 1,
          timenav_height: 220,
          hash_bookmark: true,
          lang: "en",
        },
      );
    }

    mount().catch(() => {
      if (containerRef.current) {
        containerRef.current.innerHTML =
          '<p class="p-4 text-sm text-muted">Could not load Timeline JS. Check your network connection and reload.</p>';
      }
    });

    return () => {
      cancelled = true;
      timelineRef.current?.destroy?.();
      timelineRef.current = null;
    };
  }, [containerId]);

  return (
    <div className="knight-lab-timeline -mx-4 w-[calc(100%+2rem)] sm:-mx-5 sm:w-[calc(100%+2.5rem)] lg:relative lg:left-1/2 lg:w-screen lg:max-w-none lg:-translate-x-1/2">
      <p className="mx-4 mb-3 text-sm text-muted sm:mx-5">
        {data.events.length.toLocaleString()} cosmographs on an interactive timeline — drag the
        navigation strip or click any marker. Powered by{" "}
        <a
          href="https://timeline.knightlab.com/"
          target="_blank"
          rel="noopener noreferrer"
          className="text-accent-ink underline"
        >
          Timeline JS
        </a>
        .
      </p>
      <div
        id={containerId}
        ref={containerRef}
        className="min-h-[36rem] w-full border-y border-border bg-canvas sm:min-h-[40rem]"
        style={{ height: "650px" }}
      />
    </div>
  );
}

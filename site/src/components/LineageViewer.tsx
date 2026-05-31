"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import * as d3 from "d3";
import type { LineageNodeOut, LineageOut } from "@/lib/types";
import { entityHref } from "@/lib/types";
import { lifespan } from "@/lib/format";
import {
  clampLineageZoom,
  LINEAGE_VIEW_MODE_KEY,
  LINEAGE_ZOOM_DEFAULT,
  LINEAGE_ZOOM_MAX,
  LINEAGE_ZOOM_MIN,
  LINEAGE_ZOOM_STEP,
  type LineageViewMode,
  readLineageViewMode,
} from "@/lib/lineage";

type TreeDatum = {
  id: string;
  label: string;
  href: string;
  dates: string | null;
  predicate: string | null;
  children?: TreeDatum[];
};

type TreeOrientation = "horizontal" | "vertical";

const NODE_W = 168;
const NODE_H = 52;
const GAP_X = 72;
const GAP_Y = 24;
const CANVAS_PAD_TOP = 48;
const CANVAS_PAD_BOTTOM = 16;

type TreeLayoutSize = { width: number; height: number };

function toTreeDatum(node: LineageNodeOut): TreeDatum {
  return {
    id: node.entity.id,
    label: node.entity.label,
    href: entityHref(node.entity),
    dates: lifespan(node.entity.valid_from, node.entity.valid_to),
    predicate: node.predicate,
    children: node.children.length > 0 ? node.children.map(toTreeDatum) : undefined,
  };
}

function buildTreeData(roots: LineageNodeOut[]): TreeDatum | null {
  if (roots.length === 0) return null;
  if (roots.length === 1) return toTreeDatum(roots[0]);
  return {
    id: "__root__",
    label: "",
    href: "#",
    dates: null,
    predicate: null,
    children: roots.map(toTreeDatum),
  };
}

function ViewModeToolbar({
  mode,
  onChange,
}: {
  mode: LineageViewMode;
  onChange: (mode: LineageViewMode) => void;
}) {
  const btn = (active: boolean) =>
    `rounded p-1.5 transition-colors ${
      active
        ? "bg-canvas text-ink"
        : "text-muted hover:bg-canvas hover:text-ink"
    }`;

  return (
    <div className="inline-flex items-center gap-1 rounded border border-border bg-surface p-1">
      <button
        type="button"
        aria-label="Horizontal tree view"
        aria-pressed={mode === "horizontal"}
        title="Horizontal view"
        className={btn(mode === "horizontal")}
        onClick={() => onChange("horizontal")}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          style={{ transform: "rotate(-90deg)" }}
          aria-hidden="true"
        >
          <rect x="16" y="16" width="6" height="6" rx="1" />
          <rect x="2" y="16" width="6" height="6" rx="1" />
          <rect x="9" y="2" width="6" height="6" rx="1" />
          <path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3" />
          <path d="M12 12V8" />
        </svg>
      </button>
      <button
        type="button"
        aria-label="Vertical tree view"
        aria-pressed={mode === "vertical"}
        title="Vertical view"
        className={btn(mode === "vertical")}
        onClick={() => onChange("vertical")}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <rect x="16" y="16" width="6" height="6" rx="1" />
          <rect x="2" y="16" width="6" height="6" rx="1" />
          <rect x="9" y="2" width="6" height="6" rx="1" />
          <path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3" />
          <path d="M12 12V8" />
        </svg>
      </button>
      <button
        type="button"
        aria-label="List view"
        aria-pressed={mode === "list"}
        title="List view"
        className={btn(mode === "list")}
        onClick={() => onChange("list")}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <line x1="8" y1="6" x2="21" y2="6" />
          <line x1="8" y1="12" x2="21" y2="12" />
          <line x1="8" y1="18" x2="21" y2="18" />
          <line x1="3" y1="6" x2="3.01" y2="6" />
          <line x1="3" y1="12" x2="3.01" y2="12" />
          <line x1="3" y1="18" x2="3.01" y2="18" />
        </svg>
      </button>
    </div>
  );
}

function ZoomControls({
  zoom,
  onZoomIn,
  onZoomOut,
  onReset,
}: {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
}) {
  const btn =
    "flex h-8 w-8 items-center justify-center rounded text-muted transition-colors hover:bg-canvas hover:text-ink disabled:opacity-40 disabled:hover:bg-transparent disabled:hover:text-muted";

  return (
    <div
      className="inline-flex flex-col overflow-hidden rounded border border-border bg-surface"
      role="group"
      aria-label="Zoom controls"
    >
      <button
        type="button"
        className={btn}
        aria-label="Zoom in"
        title="Zoom in"
        disabled={zoom >= LINEAGE_ZOOM_MAX}
        onClick={onZoomIn}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          aria-hidden="true"
        >
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>
      <button
        type="button"
        className={`${btn} border-y border-border text-[11px] font-medium tabular-nums`}
        aria-label="Reset zoom"
        title="Reset zoom"
        onClick={onReset}
      >
        {Math.round(zoom * 100)}%
      </button>
      <button
        type="button"
        className={btn}
        aria-label="Zoom out"
        title="Zoom out"
        disabled={zoom <= LINEAGE_ZOOM_MIN}
        onClick={onZoomOut}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          aria-hidden="true"
        >
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>
    </div>
  );
}

function LineageTreeCanvas({
  treeData,
  orientation,
  onLayout,
}: {
  treeData: TreeDatum;
  orientation: TreeOrientation;
  onLayout?: (size: TreeLayoutSize) => void;
}) {
  const router = useRouter();
  const ref = useRef<SVGSVGElement>(null);

  useEffect(() => {
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();

    const root = d3.hierarchy(treeData, (d) => d.children);
    const layout = d3.tree<TreeDatum>();
    const horizontal = orientation === "horizontal";
    layout.nodeSize(
      horizontal ? [NODE_H + GAP_Y, NODE_W + GAP_X] : [NODE_W + GAP_X, NODE_H + GAP_Y],
    );
    layout(root);

    const nodes = root
      .descendants()
      .filter((d) => d.data.id !== "__root__") as d3.HierarchyPointNode<TreeDatum>[];
    const links = root
      .links()
      .filter((l) => l.source.data.id !== "__root__" && l.target.data.id !== "__root__") as d3.HierarchyPointLink<TreeDatum>[];

    const pad = 32;
    let width: number;
    let height: number;
    let offsetX: number;
    let offsetY: number;

    if (horizontal) {
      const xs = nodes.map((d) => d.y ?? 0);
      const ys = nodes.map((d) => d.x ?? 0);
      const maxX = Math.max(...xs, 0);
      const maxY = Math.max(...ys, 0);
      const minY = Math.min(...ys, 0);
      width = Math.max(640, maxX + NODE_W + pad * 2);
      height = Math.max(320, maxY - minY + NODE_H + pad * 2);
      offsetX = pad;
      offsetY = pad - minY;
    } else {
      const xs = nodes.map((d) => d.x ?? 0);
      const ys = nodes.map((d) => d.y ?? 0);
      const maxX = Math.max(...xs, 0);
      const maxY = Math.max(...ys, 0);
      const minX = Math.min(...xs, 0);
      width = Math.max(640, maxX - minX + NODE_W + pad * 2);
      height = Math.max(420, maxY + NODE_H + pad * 2);
      offsetX = pad - minX;
      offsetY = pad;
    }

    svg.attr("width", width).attr("height", height);
    onLayout?.({ width, height });

    const linkGen = horizontal
      ? d3
          .linkHorizontal<d3.HierarchyPointLink<TreeDatum>, d3.HierarchyPointNode<TreeDatum>>()
          .x((d) => d.y + offsetX)
          .y((d) => d.x + offsetY + NODE_H / 2)
      : d3
          .linkVertical<d3.HierarchyPointLink<TreeDatum>, d3.HierarchyPointNode<TreeDatum>>()
          .x((d) => d.x + offsetX + NODE_W / 2)
          .y((d) => d.y + offsetY);

    svg
      .append("g")
      .attr("fill", "none")
      .attr("stroke", "var(--border)")
      .attr("stroke-width", 1.5)
      .selectAll("path")
      .data(links)
      .join("path")
      .attr("d", linkGen);

    const node = svg
      .append("g")
      .selectAll<SVGGElement, d3.HierarchyPointNode<TreeDatum>>("g")
      .data(nodes)
      .join("g")
      .attr(
        "transform",
        (d) =>
          horizontal
            ? `translate(${d.y + offsetX},${d.x + offsetY})`
            : `translate(${d.x + offsetX},${d.y + offsetY})`,
      )
      .attr("cursor", "pointer")
      .attr("tabindex", 0)
      .attr("role", "link")
      .attr("aria-label", (d) => d.data.label)
      .on("click", (_e, d) => router.push(d.data.href))
      .on("keydown", (e: KeyboardEvent, d) => {
        if (e.key === "Enter" || e.key === " ") router.push(d.data.href);
      });

    node
      .append("rect")
      .attr("width", NODE_W)
      .attr("height", NODE_H)
      .attr("rx", 6)
      .attr("fill", "var(--canvas)")
      .attr("stroke", "var(--border)")
      .attr("stroke-width", 1);

    node
      .append("text")
      .attr("x", NODE_W / 2)
      .attr("y", 18)
      .attr("text-anchor", "middle")
      .attr("font-size", 12)
      .attr("font-weight", 600)
      .attr("fill", "var(--ink)")
      .text((d) => {
        const label = d.data.label;
        return label.length > 22 ? `${label.slice(0, 21)}…` : label;
      });

    node
      .append("text")
      .attr("x", NODE_W / 2)
      .attr("y", 34)
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .attr("fill", "var(--muted)")
      .text((d) => d.data.dates ?? "");

    if (horizontal) {
      node
        .filter((d) => Boolean(d.data.predicate))
        .append("text")
        .attr("x", -8)
        .attr("y", NODE_H / 2 + 4)
        .attr("text-anchor", "end")
        .attr("font-size", 9)
        .attr("fill", "var(--muted)")
        .text((d) => (d.data.predicate ?? "").replace(/_/g, " "));
    }
  }, [treeData, orientation, router, onLayout]);

  return (
    <svg
      ref={ref}
      aria-label={`Transmission lineage tree (${orientation})`}
      className="min-w-full"
    />
  );
}

function countTreeNodes(nodes: LineageNodeOut[]): number {
  return nodes.reduce((total, node) => total + 1 + countTreeNodes(node.children), 0);
}

function isInfluencedPredicate(predicate: string | null | undefined): boolean {
  if (!predicate) return false;
  return predicate.toLowerCase().includes("influenc");
}

function listConnectorBorderClass(
  influenced: boolean,
  sides: "corner" | "vertical" | "horizontal",
): string {
  const color = influenced ? "border-muted" : "border-ink";
  const dash = influenced ? "border-dashed" : "border-solid";
  const width = sides === "corner" ? "border-b border-l" : "border";
  return `${width} ${color} ${dash}`;
}

function listConnectorFillClass(influenced: boolean): string {
  return influenced ? "bg-muted" : "bg-ink";
}

function LineageListNode({
  node,
  depth,
  isLastSibling,
  collapsedIds,
  onToggleCollapse,
  onNavigate,
}: {
  node: LineageNodeOut;
  depth: number;
  isLastSibling: boolean;
  collapsedIds: Set<string>;
  onToggleCollapse: (id: string) => void;
  onNavigate: (href: string) => void;
}) {
  const dates = lifespan(node.entity.valid_from, node.entity.valid_to);
  const hasChildren = node.children.length > 0;
  const isCollapsed = collapsedIds.has(node.entity.id);
  const incomingInfluenced = isInfluencedPredicate(node.predicate);

  return (
    <li className="relative" data-lineage-node={node.entity.id}>
      {depth > 0 && (
        <>
          {!isLastSibling && (
            <span
              aria-hidden="true"
              className={`pointer-events-none absolute -left-[17px] top-0 h-full w-px ${listConnectorFillClass(incomingInfluenced)}`}
            />
          )}
          <span
            aria-hidden="true"
            className={`pointer-events-none absolute -left-[17px] top-0 h-3 w-[17px] rounded-bl-[8px] ${listConnectorBorderClass(
              incomingInfluenced,
              "corner",
            )}`}
          />
        </>
      )}
      <div className="flex h-6 items-center gap-1">
        <span aria-hidden="true" className="relative inline-block h-5 w-1.5">
          <span
            className={`absolute left-0 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full ${listConnectorFillClass(false)} ${
              hasChildren ? "h-2 w-2" : "h-1.5 w-1.5"
            }`}
          />
          {hasChildren && !isCollapsed && (
            <span
              aria-hidden="true"
              className={`pointer-events-none absolute left-0 top-1/2 h-[22px] -translate-x-1/2 w-px ${listConnectorFillClass(false)}`}
            />
          )}
        </span>
        <button
          type="button"
          className="whitespace-nowrap text-left text-[13px] leading-5 text-ink/90 hover:text-ink hover:underline"
          onClick={() => onNavigate(entityHref(node.entity))}
        >
          {node.entity.label}
          {dates && <span className="ml-1.5 text-muted">{dates}</span>}
        </button>
      </div>
      {hasChildren && (
        <div className="flex h-5 items-center gap-1">
          <div className="relative inline-flex h-5 w-1.5 items-center">
            <button
              type="button"
              aria-label={isCollapsed ? "Expand descendants" : "Collapse descendants"}
              title={isCollapsed ? "Expand descendants" : "Collapse descendants"}
              className="absolute left-0 top-1/2 z-10 inline-flex h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border border-ink bg-ink text-canvas hover:bg-ink/90"
              onClick={() => onToggleCollapse(node.entity.id)}
            >
              <span aria-hidden="true" className="absolute h-px w-1.5 bg-current" />
              {isCollapsed && (
                <span aria-hidden="true" className="absolute h-1.5 w-px bg-current" />
              )}
            </button>
            {!isCollapsed && (
              <span
                aria-hidden="true"
                className={`pointer-events-none absolute left-0 top-1/2 z-0 h-2.5 -translate-x-1/2 w-px ${listConnectorFillClass(false)}`}
              />
            )}
          </div>
          <span aria-hidden="true" className="inline-block h-5 w-5" />
        </div>
      )}
      {hasChildren && !isCollapsed && (
        <ul className="relative ml-[16.5px]">
          {node.children.map((child, childIndex) => (
            <LineageListNode
              key={child.entity.id}
              node={child}
              depth={depth + 1}
              isLastSibling={childIndex === node.children.length - 1}
              collapsedIds={collapsedIds}
              onToggleCollapse={onToggleCollapse}
              onNavigate={onNavigate}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

function LineageListView({
  roots,
  unlinked,
  onNavigate,
}: {
  roots: LineageNodeOut[];
  unlinked: LineageOut["unlinked"];
  onNavigate: (href: string) => void;
}) {
  const [collapsedIds, setCollapsedIds] = useState<Set<string>>(() => new Set());
  const connectedCount = countTreeNodes(roots);

  const onToggleCollapse = useCallback((id: string) => {
    setCollapsedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  return (
    <div className="min-w-max pb-6 pl-4 pr-4 pt-14">
      <div className="mb-3 flex items-baseline gap-2">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">Lineage list</h2>
        <span className="text-xs text-muted tabular-nums">
          {connectedCount} figure{connectedCount === 1 ? "" : "s"}
        </span>
      </div>
      <ul>
        {roots.map((root, index) => (
          <LineageListNode
            key={root.entity.id}
            node={root}
            depth={0}
            isLastSibling={index === roots.length - 1}
            collapsedIds={collapsedIds}
            onToggleCollapse={onToggleCollapse}
            onNavigate={onNavigate}
          />
        ))}
      </ul>
      {unlinked.length > 0 && (
        <div className="mt-8 border-t border-border pt-6">
          <div className="mb-3 flex items-baseline gap-2">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-muted">
              Unlinked tradition members
            </h2>
            <span className="text-xs text-muted tabular-nums">{unlinked.length}</span>
          </div>
          <p className="mb-4 max-w-3xl text-sm text-muted">
            Documented in this lineage but not yet connected to the transmission tree.
          </p>
          <ul className="grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
            {unlinked.map((e) => (
              <li key={e.id} data-lineage-node={e.id}>
                <button
                  type="button"
                  onClick={() => onNavigate(entityHref(e))}
                  className="w-full rounded border border-dashed border-border px-3 py-2 text-left text-[13px] leading-5 text-ink/90 hover:text-ink hover:underline"
                >
                  {e.label}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export function LineageViewer({ lineage }: { lineage: LineageOut }) {
  const router = useRouter();
  const [mode, setModeState] = useState<LineageViewMode>("horizontal");
  const [zoom, setZoom] = useState(LINEAGE_ZOOM_DEFAULT);
  const [treeSize, setTreeSize] = useState<TreeLayoutSize>({ width: 640, height: 360 });

  useEffect(() => {
    setModeState(readLineageViewMode());
  }, []);

  useEffect(() => {
    setZoom(LINEAGE_ZOOM_DEFAULT);
  }, [mode, lineage.chart.id]);

  const setViewMode = useCallback((next: LineageViewMode) => {
    setModeState(next);
    window.localStorage.setItem(LINEAGE_VIEW_MODE_KEY, next);
  }, []);

  const zoomIn = useCallback(
    () => setZoom((z) => clampLineageZoom(z + LINEAGE_ZOOM_STEP)),
    [],
  );
  const zoomOut = useCallback(
    () => setZoom((z) => clampLineageZoom(z - LINEAGE_ZOOM_STEP)),
    [],
  );
  const resetZoom = useCallback(() => setZoom(LINEAGE_ZOOM_DEFAULT), []);

  const handleWheel = useCallback((e: React.WheelEvent<HTMLDivElement>) => {
    if (!e.ctrlKey && !e.metaKey) return;
    e.preventDefault();
    setZoom((z) => clampLineageZoom(z + (e.deltaY < 0 ? LINEAGE_ZOOM_STEP : -LINEAGE_ZOOM_STEP)));
  }, []);

  const treeData = useMemo(() => buildTreeData(lineage.roots), [lineage.roots]);
  const onNavigate = useCallback((href: string) => router.push(href), [router]);

  const showUnlinkedInTree = mode !== "list" && lineage.unlinked.length > 0;
  const isTreeMode = mode === "horizontal" || mode === "vertical";
  const scaledTreeHeight = treeSize.height + CANVAS_PAD_TOP + CANVAS_PAD_BOTTOM;

  return (
    <div className="relative">
      <div className="absolute left-3 top-3 z-10">
        <ViewModeToolbar mode={mode} onChange={setViewMode} />
      </div>

      {isTreeMode && treeData && (
        <div className="absolute bottom-3 right-3 z-10">
          <ZoomControls zoom={zoom} onZoomIn={zoomIn} onZoomOut={zoomOut} onReset={resetZoom} />
        </div>
      )}

      <div
        onWheel={isTreeMode ? handleWheel : undefined}
        className="site-scroll overflow-auto rounded-lg border border-border bg-surface min-h-[360px] max-h-[70vh]"
      >
        {!treeData ? (
          <p className="p-6 pt-14 text-sm text-muted">
            No transmission relationships documented for this lineage yet.
          </p>
        ) : mode === "list" ? (
          <LineageListView roots={lineage.roots} unlinked={lineage.unlinked} onNavigate={onNavigate} />
        ) : (
          <div
            style={{
              width: Math.ceil(treeSize.width * zoom),
              height: Math.ceil(scaledTreeHeight * zoom),
            }}
          >
            <div
              style={{
                transform: `scale(${zoom})`,
                transformOrigin: "0 0",
                width: treeSize.width,
                height: scaledTreeHeight,
              }}
            >
              <div className="pt-12 pb-4">
                <LineageTreeCanvas
                  treeData={treeData}
                  orientation={mode}
                  onLayout={setTreeSize}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {showUnlinkedInTree && (
        <div className="mt-4 rounded-lg border border-border bg-surface p-4">
          <h3 className="mb-2 text-xs font-medium uppercase tracking-wide text-muted">
            Documented figures not in tree
          </h3>
          <ul className="flex flex-wrap gap-2 text-sm">
            {lineage.unlinked.map((e) => (
              <li key={e.id}>
                <button
                  type="button"
                  onClick={() => onNavigate(entityHref(e))}
                  className="rounded-full border border-border px-3 py-1 text-muted transition-colors hover:border-accent hover:text-ink"
                >
                  {e.label}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

"use client";

import { useEffect, useMemo, useRef } from "react";
import { useRouter } from "next/navigation";
import * as d3 from "d3";
import type { GraphOut } from "@/lib/types";
import { entityHref } from "@/lib/types";

type SimNode = { id: string; label: string; type: string; href: string; root: boolean } & d3.SimulationNodeDatum;
type SimLink = { source: string; target: string; predicate: string } & d3.SimulationLinkDatum<SimNode>;

// Monochromatic ramp — mid-grays that read on both light and dark canvases.
const PALETTE = ["#737373", "#8a8a8a", "#a3a3a3", "#5c5c5c", "#bdbdbd", "#969696", "#666666"];

export function GraphExplorer({ graph, rootId }: { graph: GraphOut; rootId: string }) {
  const router = useRouter();
  const ref = useRef<SVGSVGElement>(null);

  const { nodes, links, color } = useMemo(() => {
    const types = [...new Set(graph.nodes.map((n) => n.type))];
    const color = d3.scaleOrdinal<string, string>().domain(types).range(PALETTE);
    const nodes: SimNode[] = graph.nodes.map((n) => ({
      id: n.id,
      label: n.label,
      type: n.type,
      href: entityHref(n),
      root: n.id === rootId,
    }));
    const links: SimLink[] = graph.edges.map((e) => ({
      source: e.subject_id,
      target: e.object_id,
      predicate: e.predicate,
    }));
    return { nodes, links, color };
  }, [graph, rootId]);

  useEffect(() => {
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();
    const width = ref.current?.clientWidth ?? 640;
    const height = 420;

    const sim = d3
      .forceSimulation<SimNode>(nodes)
      .force("link", d3.forceLink<SimNode, SimLink>(links).id((d) => d.id).distance(90))
      .force("charge", d3.forceManyBody().strength(-260))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide(28));

    const link = svg
      .append("g")
      .attr("stroke", "var(--border)")
      .attr("stroke-width", 1.5)
      .selectAll("line")
      .data(links)
      .join("line");

    const node = svg
      .append("g")
      .selectAll<SVGGElement, SimNode>("g")
      .data(nodes)
      .join("g")
      .attr("cursor", "pointer")
      .attr("tabindex", 0)
      .attr("role", "link")
      .attr("aria-label", (d) => d.label)
      .on("click", (_e, d) => router.push(d.href))
      .on("keydown", (e: KeyboardEvent, d) => {
        if (e.key === "Enter" || e.key === " ") router.push(d.href);
      });

    node
      .append("circle")
      .attr("r", (d) => (d.root ? 11 : 7))
      .attr("fill", (d) => (d.root ? "var(--accent)" : color(d.type)))
      .attr("stroke", "var(--surface)")
      .attr("stroke-width", (d) => (d.root ? 3 : 2));

    node
      .append("text")
      .text((d) => d.label)
      .attr("x", 12)
      .attr("y", 4)
      .attr("font-size", 12)
      .attr("font-weight", (d) => (d.root ? 600 : 400))
      .attr("fill", "var(--ink)");

    node.call(
      d3
        .drag<SVGGElement, SimNode>()
        .on("start", (event, d) => {
          if (!event.active) sim.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) sim.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }),
    );

    sim.on("tick", () => {
      link
        .attr("x1", (d) => (d.source as SimNode).x ?? 0)
        .attr("y1", (d) => (d.source as SimNode).y ?? 0)
        .attr("x2", (d) => (d.target as SimNode).x ?? 0)
        .attr("y2", (d) => (d.target as SimNode).y ?? 0);
      node.attr("transform", (d) => `translate(${d.x ?? 0},${d.y ?? 0})`);
    });

    return () => void sim.stop();
  }, [nodes, links, color, router]);

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-surface">
      <svg ref={ref} width="100%" height={420} aria-label="Entity relationship graph" />
    </div>
  );
}

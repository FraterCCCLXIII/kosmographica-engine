"""Command-line entry point for the engine: seed data and inspect the corpus.

Usage:
    kge seed mythographica <path-to-mythgraph.json> [--batch-id ID]
    kge stats
    kge eval [--gold PATH]
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

from sqlalchemy import func, select

from .adapters import (
    cosmograph_to_envelope,
    load_sqlite,
    merge_mythgraphs,
    mythographica_to_envelope,
    sacred_lineage_to_envelope,
)
from .db import session_scope
from .models import Claim, Entity, Relationship, Source
from .pipeline import ingest

_ADAPTERS = {
    "cosmograph": cosmograph_to_envelope,
    "mythographica": mythographica_to_envelope,
    "sacred_lineage": sacred_lineage_to_envelope,
}


def _load_mythgraph_dir(path: str) -> dict:
    """Merge every ``{nodes, edges}`` JSON under a directory into one graph."""
    graphs: list[dict] = []
    for fp in sorted(glob.glob(os.path.join(path, "**", "*.json"), recursive=True)):
        try:
            data = json.loads(open(fp, encoding="utf-8").read())
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and ("nodes" in data or "edges" in data):
            graphs.append(data)
    return merge_mythgraphs(graphs)


def _load_input(source: str, path: str):
    """Sacred-Lineage seeds from a SQLite DB; MythGraph from a JSON file or directory."""
    if source == "sacred_lineage":
        return load_sqlite(path)
    if source == "cosmograph":
        return json.loads(open(path, encoding="utf-8").read())
    if os.path.isdir(path):
        return _load_mythgraph_dir(path)
    return json.loads(open(path, encoding="utf-8").read())


def _cmd_seed(args: argparse.Namespace) -> int:
    adapter = _ADAPTERS.get(args.source)
    if adapter is None:
        print(f"unknown source {args.source!r}; known: {sorted(_ADAPTERS)}", file=sys.stderr)
        return 2
    data = _load_input(args.source, args.path)
    env = adapter(data, batch_id=args.batch_id)
    with session_scope() as session:
        result = ingest(session, env)
        if result.quarantined:
            print("QUARANTINED — not loaded. First errors:", file=sys.stderr)
            for issue in result.report.errors[:10]:
                print(f"  [{issue.code}] {issue.message} ({issue.where})", file=sys.stderr)
            return 1
        print(f"batch {result.batch_id}")
        for key, value in result.counts.items():
            print(f"  {key}: {value}")
    return 0


def _cmd_stats(_: argparse.Namespace) -> int:
    with session_scope() as session:
        for model, name in ((Entity, "entities"), (Relationship, "relationships"), (Claim, "claims"), (Source, "sources")):
            total = session.scalar(select(func.count()).select_from(model))
            print(f"{name}: {total}")
        print("entities by tier:")
        for tier, count in session.execute(
            select(Entity.tier, func.count()).group_by(Entity.tier)
        ).all():
            print(f"  {tier}: {count}")
    return 0


def _cmd_reconcile(args: argparse.Namespace) -> int:
    from .reconcile import accept, propose_matches, reconciliation_stats, reject

    with session_scope() as session:
        if args.action == "propose":
            summary = propose_matches(session, name_threshold=args.threshold)
            print(json.dumps(summary.as_dict(), indent=2))
        elif args.action == "accept":
            ok = accept(session, args.id)
            print("accepted" if ok else "no-op (missing or already accepted)")
            return 0 if ok else 1
        elif args.action == "reject":
            ok = reject(session, args.id, args.reason)
            print("rejected" if ok else "no-op (missing or already rejected)")
            return 0 if ok else 1
        elif args.action == "stats":
            print(json.dumps(reconciliation_stats(session), indent=2))
    return 0


def _cmd_parity(args: argparse.Namespace) -> int:
    from .reconcile import source_parity

    with session_scope() as session:
        print(json.dumps(source_parity(session, args.source), indent=2))
    return 0


def _cmd_reverify(args: argparse.Namespace) -> int:
    from .jobs import run_reverify

    with session_scope() as session:
        delta = run_reverify(
            session, batch_id=args.batch_id, generator=args.generator, tier=args.tier
        )
        print(json.dumps(delta.as_dict(), indent=2))
    return 0


def _cmd_reclassify(args: argparse.Namespace) -> int:
    from .jobs import reclassify_entities

    with session_scope() as session:
        report = reclassify_entities(
            session, source_system=args.source, dry_run=not args.apply
        )
        print(json.dumps(report.as_dict(), indent=2))
        if args.apply:
            print(f"applied: {report.changed} entities updated", file=sys.stderr)
        else:
            print(
                f"dry-run: {report.changed} entities would change "
                f"({report.flagged_for_review} flagged for review). Re-run with --apply.",
                file=sys.stderr,
            )
    return 0


def _cmd_worker(args: argparse.Namespace) -> int:
    """Inline scheduler (ADR-005: synchronous, no queue) — periodic re-verification."""
    import time

    from .jobs import run_reverify

    while True:
        with session_scope() as session:
            delta = run_reverify(
                session, batch_id=args.batch_id, generator=args.generator, tier=args.tier
            )
            print(json.dumps({"reverify": delta.as_dict()}), flush=True)
        if args.once:
            return 0
        time.sleep(args.interval)


def _cmd_eval(args: argparse.Namespace) -> int:
    from .eval import DEFAULT_GOLD, run_eval

    report = run_eval(gold_path=args.gold or DEFAULT_GOLD)
    print(json.dumps(report.as_dict(), indent=2))
    if not report.passed:
        print("FAIL: candidate verifier regressed F1 vs lexical baseline", file=sys.stderr)
        return 1
    print("PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kge")
    sub = parser.add_subparsers(dest="command", required=True)

    seed = sub.add_parser("seed", help="ingest a source dataset")
    seed.add_argument("source", choices=sorted(_ADAPTERS))
    seed.add_argument("path")
    seed.add_argument("--batch-id", default=None)
    seed.set_defaults(func=_cmd_seed)

    stats = sub.add_parser("stats", help="print corpus counts")
    stats.set_defaults(func=_cmd_stats)

    ev = sub.add_parser("eval", help="evaluate the verifier against the gold set")
    ev.add_argument("--gold", default=None, help="path to a gold JSONL file")
    ev.set_defaults(func=_cmd_eval)

    rec = sub.add_parser("reconcile", help="cross-source entity resolution (sameAs)")
    rec.add_argument("action", choices=["propose", "accept", "reject", "stats"])
    rec.add_argument("id", nargs="?", type=int, help="reconciliation id (accept/reject)")
    rec.add_argument("--reason", default=None, help="rejection reason")
    rec.add_argument("--threshold", type=float, default=0.6, help="name-match score threshold")
    rec.set_defaults(func=_cmd_reconcile)

    par = sub.add_parser("parity", help="source convergence/parity check")
    par.add_argument("source", help="source_system, e.g. sacred_lineage")
    par.set_defaults(func=_cmd_parity)

    rev = sub.add_parser("reverify", help="re-verify AI-grounded claims once (audit delta)")
    rev.add_argument("--batch-id", default=None)
    rev.add_argument("--generator", default=None)
    rev.add_argument("--tier", default=None)
    rev.set_defaults(func=_cmd_reverify)

    rc = sub.add_parser(
        "reclassify", help="recompute entity type/subtype/status against the controlled taxonomy"
    )
    rc.add_argument("--source", default="mythographica", help="source_system to reclassify")
    rc.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    rc.set_defaults(func=_cmd_reclassify)

    work = sub.add_parser("worker", help="inline scheduler: periodic re-verification (ADR-005)")
    work.add_argument("--interval", type=float, default=300.0, help="seconds between runs")
    work.add_argument("--once", action="store_true", help="run a single pass and exit")
    work.add_argument("--batch-id", default=None)
    work.add_argument("--generator", default=None)
    work.add_argument("--tier", default=None)
    work.set_defaults(func=_cmd_worker)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

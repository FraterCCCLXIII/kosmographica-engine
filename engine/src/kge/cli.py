"""Command-line entry point for the engine: seed data and inspect the corpus.

Usage:
    kge seed mythographica <path-to-mythgraph.json> [--batch-id ID]
    kge stats
"""

from __future__ import annotations

import argparse
import json
import sys

from sqlalchemy import func, select

from .adapters import mythographica_to_envelope
from .db import session_scope
from .models import Claim, Entity, Relationship, Source
from .pipeline import ingest

_ADAPTERS = {"mythographica": mythographica_to_envelope}


def _cmd_seed(args: argparse.Namespace) -> int:
    adapter = _ADAPTERS.get(args.source)
    if adapter is None:
        print(f"unknown source {args.source!r}; known: {sorted(_ADAPTERS)}", file=sys.stderr)
        return 2
    graph = json.loads(open(args.path, encoding="utf-8").read())
    env = adapter(graph, batch_id=args.batch_id)
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

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

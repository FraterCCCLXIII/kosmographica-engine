"""Background jobs (ADR-005).

Inline/synchronous by decision — no Redis/queue until ingestion or embedding
workloads force it. The re-verification job recomputes confidence/tier for
AI-grounded claims using the configured verifier and emits an audit delta.
"""

from .reclassify import ReclassifyReport, reclassify_entities
from .reverify import ReverifyDelta, run_reverify

__all__ = ["run_reverify", "ReverifyDelta", "reclassify_entities", "ReclassifyReport"]

"""Cross-source entity resolution (Wave 2 / W2.2, entity-resolution.md).

Produces ``sameAs`` *proposals* between entities from different source systems.
Never destructive: deterministic external-ID matches auto-link; scored name
matches go to a review queue. Honors the non-negotiables — conflicts keep both
claims, and there is no cross-tradition auto-merge on name alone.
"""

from .engine import accept, propose_matches, reconciliation_stats, reject
from .parity import source_parity

__all__ = ["propose_matches", "accept", "reject", "reconciliation_stats", "source_parity"]

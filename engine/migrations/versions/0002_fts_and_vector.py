"""FTS index + pgvector embedding column

Revision ID: 0002_fts_vector
Revises: 4e5c94684bcc
Create Date: 2026-05-30
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "0002_fts_vector"
down_revision: Union[str, None] = "4e5c94684bcc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Shared FTS expression — keep in sync with kge.search.FTS_SQL.
_FTS_EXPR = (
    "to_tsvector('simple', coalesce(label, '') || ' ' || coalesce(data->>'description', ''))"
)


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("ALTER TABLE entities ADD COLUMN IF NOT EXISTS embedding vector(384)")
    op.execute(f"CREATE INDEX IF NOT EXISTS ix_entities_fts ON entities USING GIN ({_FTS_EXPR})")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_entities_fts")
    op.execute("ALTER TABLE entities DROP COLUMN IF EXISTS embedding")

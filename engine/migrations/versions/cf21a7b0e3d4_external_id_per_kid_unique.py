"""external_id uniqueness per-KID (enable shared external ids across sources)

Revision ID: cf21a7b0e3d4
Revises: bc8c0fc807ec
Create Date: 2026-05-30 14:45:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "cf21a7b0e3d4"
down_revision: Union[str, None] = "bc8c0fc807ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_external_authority_value", "external_ids", type_="unique")
    op.create_unique_constraint(
        "uq_external_kid_authority_value", "external_ids", ["kid", "authority", "value"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_external_kid_authority_value", "external_ids", type_="unique")
    op.create_unique_constraint(
        "uq_external_authority_value", "external_ids", ["authority", "value"]
    )

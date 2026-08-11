"""add notifications_enabled to users

Revision ID: 5d6f7a8b9c10
Revises: 1e5d1b9b2f5a
Create Date: 2026-04-02 01:10:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5d6f7a8b9c10"
down_revision: Union[str, Sequence[str], None] = "1e5d1b9b2f5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "notifications_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    op.alter_column("users", "notifications_enabled", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "notifications_enabled")

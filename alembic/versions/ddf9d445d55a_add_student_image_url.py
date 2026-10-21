
"""add student image URL

Revision ID: ddf9d445d55a
Revises:
Create Date: 2026-10-20 12:12:55.824797
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ddf9d445d55a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the student image URL column."""
    op.add_column(
        "students",
        sa.Column("img_URL", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Remove the student image URL column."""
    op.drop_column("students", "img_URL")

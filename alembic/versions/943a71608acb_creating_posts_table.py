"""Creating Posts Table

Revision ID: 943a71608acb
Revises: 
Create Date: 2026-09-22 20:47:24.417074

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '943a71608acb'
down_revision: Union[str, Sequence[str], None] = None  # noqa: UP007
branch_labels: Union[str, Sequence[str], None] = None  # noqa: UP007
depends_on: Union[str, Sequence[str], None] = None  # noqa: UP007


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                            sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    pass  # noqa: PIE790

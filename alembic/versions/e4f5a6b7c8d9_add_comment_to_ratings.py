"""add comment to ratings

Revision ID: e4f5a6b7c8d9
Revises: 70c3d7ede669
Create Date: 2026-09-29 22:18:20.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4f5a6b7c8d9'
down_revision: Union[str, None] = '70c3d7ede669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('ratings', sa.Column('comment', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('ratings', 'comment')

"""empty message

Revision ID: 6791f0e85943
Revises: 3430aeb39371
Create Date: 2024-03-18 21:09:36.817806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6791f0e85943'
down_revision: Union[str, None] = '3430aeb39371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('anime', 'status')
    animetype_enum = postgresql.ENUM('PENDING', 'CONFIRMED', 'QUARANTINE', name='ReviewStatus', create_type=False)
    animetype_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('anime', sa.Column('status', animetype_enum, nullable=False))


def downgrade() -> None:
    op.drop_column('anime', 'status')
    op.add_column('anime', sa.Column('status', sa.Enum('pending', 'confirmed', 'quarantine', name='ReviewStatus'),
              nullable=False))

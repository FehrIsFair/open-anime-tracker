"""empty message

Revision ID: 62bacc658daa
Revises: 6791f0e85943
Create Date: 2024-03-25 22:00:50.385236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62bacc658daa'
down_revision: Union[str, None] = '6791f0e85943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anime', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('anime', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('anime', sa.Column('rank', sa.Integer(), nullable=True))
    op.add_column('anime', sa.Column('content_rating', sa.String(), nullable=True))
    op.add_column('anime', sa.Column('nsfw', sa.Boolean(), nullable=True))
    op.add_column('seasons', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('seasons', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('seasons', sa.Column('air_date', sa.String(), nullable=True))
    op.add_column('seasons', sa.Column('end_date', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seasons', 'end_date')
    op.drop_column('seasons', 'air_date')
    op.drop_column('seasons', 'updated_at')
    op.drop_column('seasons', 'created_at')
    op.drop_column('anime', 'nsfw')
    op.drop_column('anime', 'content_rating')
    op.drop_column('anime', 'rank')
    op.drop_column('anime', 'updated_at')
    op.drop_column('anime', 'created_at')
    # ### end Alembic commands ###
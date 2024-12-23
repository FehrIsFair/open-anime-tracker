"""empty message

Revision ID: 8b3127c1ce0a
Revises: 55d1dc0895fe
Create Date: 2024-12-23 14:57:01.065230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b3127c1ce0a'
down_revision: Union[str, None] = '55d1dc0895fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seasons', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seasons', 'title')
    # ### end Alembic commands ###

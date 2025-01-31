"""empty message

Revision ID: 55d1dc0895fe
Revises: 505bdba43992
Create Date: 2024-12-23 02:08:44.415977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic.ddl import postgresql

from enums.db_enums import SeasonType

# revision identifiers, used by Alembic.
revision: str = '55d1dc0895fe'
down_revision: Union[str, None] = '505bdba43992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    seasontype_enum = sa.Enum('SEASON', 'ONA', 'OVA', 'SPECIAL', name='seasontype', create_type=False)
    op.execute("ALTER TYPE seasontype ADD VALUE 'SPECIAL'")
    op.alter_column('seasons', str(sa.Column('type_season', seasontype_enum, nullable=False)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    seasontype_enum = sa.Enum('SEASON', 'ONA', 'OVA', name='seasontype', create_type=False)
    op.execute("ALTER TYPE user_status DROP VALUE 'SPECIAL'")
    op.alter_column('seasontype', str(sa.String('type_season', seasontype_enum, nullable=False)))
    # ### end Alembic commands ###

"""add status and timestamps to lists

Revision ID: f5a6b7c8d9e0
Revises: e4f5a6b7c8d9
Create Date: 2026-10-07 23:30:00.000000

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f5a6b7c8d9e0'
down_revision: str | None = 'e4f5a6b7c8d9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    list_status_enum = postgresql.ENUM(
        'plan_to_watch',
        'watching',
        'complete',
        'dropped',
        'on_hold',
        name='liststatus',
        create_type=False,
    )
    list_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'lists',
        sa.Column(
            'status',
            list_status_enum,
            nullable=False,
            server_default='plan_to_watch',
        ),
    )
    op.add_column(
        'lists',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text('now()'),
        ),
    )
    op.add_column(
        'lists',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text('now()'),
        ),
    )
    op.create_unique_constraint(
        'uq_user_anime_list',
        'lists',
        ['user_id', 'anime_id'],
    )


def downgrade() -> None:
    op.drop_constraint('uq_user_anime_list', 'lists', type_='unique')
    op.drop_column('lists', 'updated_at')
    op.drop_column('lists', 'created_at')
    op.drop_column('lists', 'status')
    sa.Enum(
        'plan_to_watch',
        'watching',
        'complete',
        'dropped',
        'on_hold',
        name='liststatus',
    ).drop(op.get_bind(), checkfirst=True)

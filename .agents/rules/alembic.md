# Alembic Migrations — Rules

This directory contains all Alembic migration scripts for Open Anime Tracker.

## Conventions

### File Structure

Migrations follow the template in `script.py.mako`:

```python
"""<message>

Revision ID: <id>
Revises: <parent>
Create Date: <timestamp>

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = '<id>'
down_revision: Union[str, None] = '<parent>'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    ...

def downgrade() -> None:
    ...
```

### Revision Chain

Maintain a **linear** chain (no branches). `down_revision` of each file points to the previous file's `revision` ID.

To find the latest migration, look for the file that no other file references as `down_revision`.

### Upgrade / Downgrade Pairs

Every `upgrade()` operation must have a matching `downgrade()` that reverses it in **reverse order**:

| Upgrade | Downgrade |
|---|---|
| `op.create_table('t', ...)` | `op.drop_table('t')` |
| `op.add_column('t', c)` | `op.drop_column('t', 'c')` |
| `op.drop_column('t', 'c')` | `op.add_column('t', c)` |
| `op.create_index('ix', 't', ['c'])` | `op.drop_index('ix', table_name='t')` |
| `op.alter_column('t', 'c', nullable=True)` | `op.alter_column('t', 'c', nullable=False)` |
| Enum creation → column add | Column drop → enum drop |

### Enum Handling (PostgreSQL)

When adding or modifying an enum column:

**Upgrade:**
```python
from sqlalchemy.dialects import postgresql

my_enum = postgresql.ENUM('a', 'b', 'c', name='MyEnum', create_type=False)
my_enum.create(op.get_bind(), checkfirst=True)
op.add_column('table', sa.Column('col', my_enum, nullable=False))
```

**Downgrade:**
```python
op.drop_column('table', 'col')
sa.Enum('a', 'b', 'c', name='MyEnum').drop(op.get_bind(), checkfirst=True)
```

Rules:
- Use `postgresql.ENUM` for the upgrade, `sa.Enum` for the downgrade drop.
- `create_type=False` — avoids re-creating on every run.
- `checkfirst=True` — idempotent.
- Downgrade: drop the **column** before dropping the **enum type**.

### Table / Column References

- Table names match `__tablename__` from the models: `'users'`, `'anime'`, `'lists'`, `'ratings'', 'seasons'`, `'invites'`.
- Column names match the Python attribute names in the corresponding model.

### Imports

Only import what you use:

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql   # only when using PG enums
```

### Migration Creation Workflow

```sh
# 1. Modify model(s) in db_models/
# 2. Generate migration
alembic revision --autogenerate -m "describe the change"

# 3. Review the generated file:
#    - Ensure upgrade and downgrade are mirrored
#    - Fix enum handling (PG-specific)
#    - Verify column types match the model
```

### Running Migrations

```sh
alembic upgrade head      # apply pending
alembic downgrade -1      # revert one step
alembic current           # check current revision
alembic history           # show chain
```

## Link to Models

- All models must be imported in `alembic/env.py` (see `import` block at top of `env.py`) for autogenerate to detect them.
- `compare_type=True` is enabled in both `run_migrations_offline()` and `run_migrations_online()` in `env.py`, so type mismatches are caught.
- Every change to `db_models/` requires a corresponding migration.

## Troubleshooting

| Problem | Fix |
|---|---|
| Autogenerate doesn't detect a model change | Ensure the model is imported in `alembic/env.py` |
| `duplicate object` error on enum | Verify `create_type=False` and the enum name matches |
| Downgrade fails | Confirm downgrade reverses every upgrade in the correct order |
| Schema drift | Compare current DB schema against `db_models/` and create corrective migrations |

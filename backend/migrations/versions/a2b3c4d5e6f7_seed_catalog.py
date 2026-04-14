"""seed catalog data: idea statuses and roles

Revision ID: a2b3c4d5e6f7
Revises: 7260f8cfa797
Create Date: 2026-04-14 00:00:00.000000

Inserts the reference data the app requires to function in ALL environments.
User/demo data is NOT included here — see scripts/seed_dev.py.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "a2b3c4d5e6f7"
down_revision: Union[str, Sequence[str], None] = "7260f8cfa797"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO idea_statuses (code, name, is_terminal, sort_order) VALUES
            ('idea',        'Idea',        false, 10),
            ('in_progress', 'In Progress', false, 20),
            ('completed',   'Completed',   true,  30)
        ON CONFLICT (code) DO UPDATE SET
            name        = EXCLUDED.name,
            is_terminal = EXCLUDED.is_terminal,
            sort_order  = EXCLUDED.sort_order
    """)

    op.execute("""
        INSERT INTO roles (name) VALUES ('admin'), ('user')
        ON CONFLICT (name) DO NOTHING
    """)


def downgrade() -> None:
    # Catalog rows are required for FK integrity — removing them would cascade-break
    # existing ideas and users. Downgrade is intentionally a no-op.
    pass

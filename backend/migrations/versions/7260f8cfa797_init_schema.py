"""init schema

Revision ID: 7260f8cfa797
Revises: 5bab06b1afdd
Create Date: 2026-04-06 07:27:27.196565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7260f8cfa797'
down_revision: Union[str, Sequence[str], None] = '5bab06b1afdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

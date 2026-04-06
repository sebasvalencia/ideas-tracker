"""init schema

Revision ID: 5bab06b1afdd
Revises: 
Create Date: 2026-04-05 20:29:32.952684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bab06b1afdd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "roles",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "idea_statuses",
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("is_terminal", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.UniqueConstraint("code", name="uq_idea_statuses_code"),
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_id", sa.BigInteger(), sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "ideas",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("owner_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status_id", sa.SmallInteger(), sa.ForeignKey("idea_statuses.id"), nullable=False),
        sa.Column("execution_percentage", sa.Numeric(5, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("execution_percentage >= 0 AND execution_percentage <= 100", name="ck_ideas_execution_percentage"),
    )

    op.create_table(
        "idea_progress_logs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("idea_id", sa.BigInteger(), sa.ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("progress_snapshot", sa.Numeric(5, 2), nullable=False),
        sa.Column("status_snapshot", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("progress_snapshot >= 0 AND progress_snapshot <= 100", name="ck_logs_progress_snapshot"),
        sa.CheckConstraint("status_snapshot IN ('idea','in_progress','completed')", name="ck_logs_status_snapshot"),
    )

    op.create_table(
        "idea_ratings",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("idea_id", sa.BigInteger(), sa.ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rating", sa.SmallInteger(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("idea_id", name="uq_idea_ratings_idea_id"),
        sa.CheckConstraint("rating BETWEEN 1 AND 10", name="ck_ratings_range"),
    )

    op.create_index(
        "ix_ideas_owner_status_created_at",
        "ideas",
        ["owner_id", "status_id", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_logs_idea_created_at",
        "idea_progress_logs",
        ["idea_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_logs_idea_created_at", table_name="idea_progress_logs")
    op.drop_index("ix_ideas_owner_status_created_at", table_name="ideas")

    op.drop_table("idea_ratings")
    op.drop_table("idea_progress_logs")
    op.drop_table("ideas")
    op.drop_table("user_roles")
    op.drop_table("idea_statuses")
    op.drop_table("users")
    op.drop_table("roles")

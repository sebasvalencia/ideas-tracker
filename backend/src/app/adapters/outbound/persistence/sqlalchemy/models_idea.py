from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, Text, SmallInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.adapters.outbound.persistence.sqlalchemy.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class Idea(Base):
    __tablename__ = "ideas"
    __table_args__ = (
        CheckConstraint("execution_percentage >= 0 AND execution_percentage <= 100", name="ck_ideas_execution_percentage"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("idea_statuses.id"), nullable=False)
    status: Mapped["IdeaStatus"] = relationship(back_populates="ideas")
    execution_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.00"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    logs: Mapped[list["IdeaProgressLog"]] = relationship(back_populates="idea", cascade="all, delete-orphan")
    rating: Mapped["IdeaRating | None"] = relationship(back_populates="idea", uselist=False, cascade="all, delete-orphan")

class IdeaStatus(Base):
    __tablename__ = "idea_statuses"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    is_terminal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    ideas: Mapped[list["Idea"]] = relationship(back_populates="status")

class IdeaProgressLog(Base):
    __tablename__ = "idea_progress_logs"
    __table_args__ = (
        CheckConstraint("progress_snapshot >= 0 AND progress_snapshot <= 100", name="ck_logs_progress_snapshot"),
        CheckConstraint("status_snapshot IN ('idea','in_progress','completed')", name="ck_logs_status_snapshot"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    idea_id: Mapped[int] = mapped_column(ForeignKey("ideas.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    progress_snapshot: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    status_snapshot: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    idea: Mapped[Idea] = relationship(back_populates="logs")


class IdeaRating(Base):
    __tablename__ = "idea_ratings"
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 10", name="ck_ratings_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    idea_id: Mapped[int] = mapped_column(ForeignKey("ideas.id", ondelete="CASCADE"), unique=True, nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    idea: Mapped[Idea] = relationship(back_populates="rating")
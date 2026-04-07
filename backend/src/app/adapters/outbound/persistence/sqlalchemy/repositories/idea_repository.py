from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload, sessionmaker

from src.app.adapters.outbound.persistence.sqlalchemy.models_idea import Idea, IdeaStatus
from src.app.application.idea.ports import IdeaRecord


class SqlAlchemyIdeaRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def create(self, *, owner_id: int, title: str, description: str) -> IdeaRecord:
        with self._session_factory() as db:
            status = db.scalar(select(IdeaStatus).where(IdeaStatus.code == "idea"))
            if status is None:
                raise ValueError("missing required idea status: idea")

            row = Idea(
                owner_id=owner_id,
                title=title,
                description=description,
                status_id=status.id,
                execution_percentage=Decimal("0.00"),
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            db.refresh(row, attribute_names=["status"])
            return self._to_record(row)

    def list_active(self, *, owner_id: int, status: str | None, limit: int, offset: int) -> list[IdeaRecord]:
        with self._session_factory() as db:
            query = (
                select(Idea)
                .options(joinedload(Idea.status))
                .join(IdeaStatus, Idea.status_id == IdeaStatus.id)
                .where(Idea.owner_id == owner_id, Idea.deleted_at.is_(None))
                .order_by(Idea.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
            if status is not None:
                query = query.where(IdeaStatus.code == status)
            rows = db.scalars(query).all()
            return [self._to_record(row) for row in rows]

    def get_active_by_id(self, *, idea_id: int) -> IdeaRecord | None:
        with self._session_factory() as db:
            row = db.scalar(
                select(Idea)
                .options(joinedload(Idea.status))
                .where(Idea.id == idea_id, Idea.deleted_at.is_(None))
            )
            return None if row is None else self._to_record(row)

    def update(self, *, idea: IdeaRecord) -> IdeaRecord:
        with self._session_factory() as db:
            row = db.scalar(select(Idea).where(Idea.id == idea.id))
            if row is None:
                raise ValueError(f"Idea with id {idea.id} not found")

            status = db.scalar(select(IdeaStatus).where(IdeaStatus.code == idea.status))
            if status is None:
                raise ValueError(f"invalid idea status: {idea.status}")

            row.owner_id = idea.owner_id
            row.title = idea.title
            row.description = idea.description
            row.status_id = status.id
            row.execution_percentage = Decimal(str(idea.execution_percentage))
            row.updated_at = idea.updated_at
            row.deleted_at = idea.deleted_at

            db.commit()
            db.refresh(row)
            db.refresh(row, attribute_names=["status"])
            return self._to_record(row)

    def soft_delete(self, *, idea_id: int, deleted_at: datetime) -> None:
        with self._session_factory() as db:
            row = db.scalar(select(Idea).where(Idea.id == idea_id))
            if row is None:
                return
            row.deleted_at = deleted_at
            row.updated_at = deleted_at
            db.commit()

    @staticmethod
    def _to_record(row: Idea) -> IdeaRecord:
        return IdeaRecord(
            id=row.id,
            owner_id=row.owner_id,
            title=row.title,
            description=row.description,
            status=row.status.code,
            execution_percentage=float(row.execution_percentage),
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
        )

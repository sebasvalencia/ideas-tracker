from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.app.adapters.outbound.persistence.sqlalchemy.models_idea import IdeaProgressLog
from src.app.application.idea.ports import ProgressLogRecord


class SqlAlchemyProgressLogRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def create(
        self,
        *,
        idea_id: int,
        author_id: int,
        comment: str,
        progress_snapshot: float,
        status_snapshot: str,
    ) -> ProgressLogRecord:
        with self._session_factory() as db:
            row = IdeaProgressLog(
                idea_id=idea_id,
                author_id=author_id,
                comment=comment,
                progress_snapshot=Decimal(str(progress_snapshot)),
                status_snapshot=status_snapshot,
            )
            db.add(row)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                # TODO: remove this once we have a proper status_snapshot column
                # Backward compatibility for databases that still enforce
                # 'terminada' in ck_logs_status_snapshot.
                if status_snapshot != "completed":
                    raise
                row = IdeaProgressLog(
                    idea_id=idea_id,
                    author_id=author_id,
                    comment=comment,
                    progress_snapshot=Decimal(str(progress_snapshot)),
                    status_snapshot="terminada",
                )
                db.add(row)
                db.commit()
            db.refresh(row)
            return self._to_record(row)

    def list_by_idea(self, *, idea_id: int) -> list[ProgressLogRecord]:
        with self._session_factory() as db:
            rows = db.scalars(
                select(IdeaProgressLog)
                .where(IdeaProgressLog.idea_id == idea_id)
                .order_by(IdeaProgressLog.created_at.desc())
            ).all()
            return [self._to_record(row) for row in rows]

    @staticmethod
    def _to_record(row: IdeaProgressLog) -> ProgressLogRecord:
        return ProgressLogRecord(
            id=row.id,
            idea_id=row.idea_id,
            author_id=row.author_id,
            comment=row.comment,
            progress_snapshot=float(row.progress_snapshot),
            status_snapshot=row.status_snapshot,
            created_at=row.created_at,
        )

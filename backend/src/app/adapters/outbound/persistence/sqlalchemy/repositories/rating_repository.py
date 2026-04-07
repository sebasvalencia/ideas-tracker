from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.app.adapters.outbound.persistence.sqlalchemy.models_idea import IdeaRating
from src.app.application.idea.ports import RatingRecord


class SqlAlchemyRatingRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def get_by_idea(self, *, idea_id: int) -> RatingRecord | None:
        with self._session_factory() as db:
            row = db.scalar(select(IdeaRating).where(IdeaRating.idea_id == idea_id))
            if row is None:
                return None
            return self._to_record(row)

    def create(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord:
        with self._session_factory() as db:
            row = IdeaRating(
                idea_id=idea_id,
                rating=rating,
                summary=summary,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return self._to_record(row)

    def update(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord:
        with self._session_factory() as db:
            row = db.scalar(select(IdeaRating).where(IdeaRating.idea_id == idea_id))
            if row is None:
                raise ValueError("rating not found")
            row.rating = rating
            row.summary = summary
            db.commit()
            db.refresh(row)
            return self._to_record(row)

    @staticmethod
    def _to_record(row: IdeaRating) -> RatingRecord:
        return RatingRecord(
            id=row.id,
            idea_id=row.idea_id,
            rating=row.rating,
            summary=row.summary,
            created_at=row.created_at,
        )

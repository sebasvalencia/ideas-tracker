from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.dto import RateIdeaInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord, RatingRecord
from src.app.application.idea.use_cases.rating import GetIdeaRatingUseCase, RateIdeaUseCase, UpdateIdeaRatingUseCase


class FakeAuthContext:
    def __init__(self, user_id: int, role: str = "user") -> None:
        self._user = AuthUser(user_id=user_id, email="tester@ideas.com", role=role)

    def current_user(self) -> AuthUser:
        return self._user


class FakeIdeaRepository:
    def __init__(self, idea: IdeaRecord | None) -> None:
        self._idea = idea

    def get_active_by_id(self, *, idea_id: int) -> IdeaRecord | None:
        if self._idea is None:
            return None
        return self._idea if self._idea.id == idea_id else None


class FakeRatingRepository:
    def __init__(self) -> None:
        self._row: RatingRecord | None = None

    def get_by_idea(self, *, idea_id: int) -> RatingRecord | None:
        if self._row is None:
            return None
        return self._row if self._row.idea_id == idea_id else None

    def create(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord:
        self._row = RatingRecord(
            id=1,
            idea_id=idea_id,
            rating=rating,
            summary=summary,
            created_at=datetime.now(),
        )
        return self._row

    def update(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord:
        if self._row is None:
            raise ValueError("rating not found")
        self._row = RatingRecord(
            id=self._row.id,
            idea_id=idea_id,
            rating=rating,
            summary=summary,
            created_at=self._row.created_at,
        )
        return self._row


def _idea(owner_id: int = 42, status: str = "completed") -> IdeaRecord:
    now = datetime.now()
    return IdeaRecord(
        id=10,
        owner_id=owner_id,
        title="Idea",
        description="Desc",
        status=status,
        execution_percentage=100.0 if status == "completed" else 10.0,
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )


def test_rate_idea_success() -> None:
    use_case = RateIdeaUseCase(
        idea_repository=FakeIdeaRepository(_idea()),
        rating_repository=FakeRatingRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    result = use_case.execute(idea_id=10, data=RateIdeaInput(rating=8, summary="ok"))
    assert result.rating == 8


def test_rate_idea_rejects_not_finished() -> None:
    use_case = RateIdeaUseCase(
        idea_repository=FakeIdeaRepository(_idea(status="in_progress")),
        rating_repository=FakeRatingRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(DomainValidationError, match="rating allowed only for finished ideas"):
        use_case.execute(idea_id=10, data=RateIdeaInput(rating=8))


def test_rate_idea_rejects_out_of_range() -> None:
    use_case = RateIdeaUseCase(
        idea_repository=FakeIdeaRepository(_idea()),
        rating_repository=FakeRatingRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(DomainValidationError, match="rating must be between 1 and 10"):
        use_case.execute(idea_id=10, data=RateIdeaInput(rating=11))


def test_update_idea_rating_success() -> None:
    ratings = FakeRatingRepository()
    ratings.create(idea_id=10, rating=7, summary=None)
    use_case = UpdateIdeaRatingUseCase(
        idea_repository=FakeIdeaRepository(_idea()),
        rating_repository=ratings,
        auth_ctx=FakeAuthContext(user_id=42),
    )
    result = use_case.execute(idea_id=10, data=RateIdeaInput(rating=9, summary="mejor"))
    assert result.rating == 9
    assert result.summary == "mejor"


def test_get_idea_rating_not_found() -> None:
    use_case = GetIdeaRatingUseCase(
        idea_repository=FakeIdeaRepository(_idea()),
        rating_repository=FakeRatingRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(NotFoundError, match="rating not found"):
        use_case.execute(idea_id=10)


def test_rate_idea_forbidden_for_non_owner_non_admin() -> None:
    use_case = RateIdeaUseCase(
        idea_repository=FakeIdeaRepository(_idea(owner_id=1)),
        rating_repository=FakeRatingRepository(),
        auth_ctx=FakeAuthContext(user_id=2),
    )
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10, data=RateIdeaInput(rating=8))

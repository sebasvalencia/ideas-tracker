from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord
from src.app.application.idea.use_cases.get_idea_detail import GetIdeaDetailUseCase


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
        if self._idea.id != idea_id:
            return None
        return self._idea


def _idea(owner_id: int = 42) -> IdeaRecord:
    now = datetime.now()
    return IdeaRecord(
        id=10,
        owner_id=owner_id,
        title="Idea title",
        description="Idea description",
        status="idea",
        execution_percentage=0.0,
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )


def test_get_idea_detail_success_for_owner() -> None:
    use_case = GetIdeaDetailUseCase(repository=FakeIdeaRepository(_idea(owner_id=42)), auth_ctx=FakeAuthContext(user_id=42))
    result = use_case.execute(idea_id=10)
    assert result.id == 10
    assert result.owner_id == 42


def test_get_idea_detail_raises_not_found() -> None:
    use_case = GetIdeaDetailUseCase(repository=FakeIdeaRepository(None), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(NotFoundError, match="idea not found"):
        use_case.execute(idea_id=999)


def test_get_idea_detail_forbidden_for_non_owner_non_admin() -> None:
    use_case = GetIdeaDetailUseCase(repository=FakeIdeaRepository(_idea(owner_id=10)), auth_ctx=FakeAuthContext(user_id=99))
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10)


def test_get_idea_detail_allows_admin() -> None:
    use_case = GetIdeaDetailUseCase(
        repository=FakeIdeaRepository(_idea(owner_id=10)),
        auth_ctx=FakeAuthContext(user_id=99, role="admin"),
    )
    result = use_case.execute(idea_id=10)
    assert result.id == 10

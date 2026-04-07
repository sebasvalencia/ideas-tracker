from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord
from src.app.application.idea.use_cases.delete_idea import DeleteIdeaUseCase


class FakeAuthContext:
    def __init__(self, user_id: int, role: str = "user") -> None:
        self._user = AuthUser(user_id=user_id, email="tester@ideas.com", role=role)

    def current_user(self) -> AuthUser:
        return self._user


class FakeIdeaRepository:
    def __init__(self, idea: IdeaRecord | None) -> None:
        self._idea = idea
        self.soft_deleted_idea_id: int | None = None

    def get_active_by_id(self, *, idea_id: int) -> IdeaRecord | None:
        if self._idea is None:
            return None
        return self._idea if self._idea.id == idea_id and self._idea.deleted_at is None else None

    def soft_delete(self, *, idea_id: int, deleted_at: datetime) -> None:
        if self._idea is None or self._idea.id != idea_id:
            return
        self._idea = IdeaRecord(
            id=self._idea.id,
            owner_id=self._idea.owner_id,
            title=self._idea.title,
            description=self._idea.description,
            status=self._idea.status,
            execution_percentage=self._idea.execution_percentage,
            created_at=self._idea.created_at,
            updated_at=deleted_at,
            deleted_at=deleted_at,
        )
        self.soft_deleted_idea_id = idea_id


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


def test_delete_soft_deletes_for_owner() -> None:
    repo = FakeIdeaRepository(_idea(owner_id=42))
    use_case = DeleteIdeaUseCase(repository=repo, auth_ctx=FakeAuthContext(user_id=42))
    use_case.execute(idea_id=10)
    assert repo.soft_deleted_idea_id == 10
    assert repo._idea is not None and repo._idea.deleted_at is not None


def test_delete_not_found_when_idea_missing() -> None:
    use_case = DeleteIdeaUseCase(repository=FakeIdeaRepository(None), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(NotFoundError, match="idea not found"):
        use_case.execute(idea_id=999)


def test_delete_forbidden_for_non_owner_non_admin() -> None:
    use_case = DeleteIdeaUseCase(repository=FakeIdeaRepository(_idea(owner_id=1)), auth_ctx=FakeAuthContext(user_id=2))
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10)

from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.dto import AddProgressLogInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord, ProgressLogRecord
from src.app.application.idea.use_cases.add_progress_log import AddProgressLogUseCase


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


class FakeLogRepository:
    def __init__(self) -> None:
        self.last_create: dict | None = None

    def create(
        self,
        *,
        idea_id: int,
        author_id: int,
        comment: str,
        progress_snapshot: float,
        status_snapshot: str,
    ) -> ProgressLogRecord:
        self.last_create = {
            "idea_id": idea_id,
            "author_id": author_id,
            "comment": comment,
            "progress_snapshot": progress_snapshot,
            "status_snapshot": status_snapshot,
        }
        return ProgressLogRecord(
            id=1,
            idea_id=idea_id,
            author_id=author_id,
            comment=comment,
            progress_snapshot=progress_snapshot,
            status_snapshot=status_snapshot,
            created_at=datetime.now(),
        )


def _idea(owner_id: int = 42) -> IdeaRecord:
    now = datetime.now()
    return IdeaRecord(
        id=10,
        owner_id=owner_id,
        title="Idea title",
        description="Idea description",
        status="in_progress",
        execution_percentage=33.0,
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )


def test_add_progress_log_uses_current_idea_snapshot() -> None:
    logs = FakeLogRepository()
    use_case = AddProgressLogUseCase(
        idea_repository=FakeIdeaRepository(_idea(owner_id=42)),
        log_repository=logs,
        auth_ctx=FakeAuthContext(user_id=42),
    )
    result = use_case.execute(idea_id=10, data=AddProgressLogInput(comment="  avance del dia  "))
    assert result.idea_id == 10
    assert result.author_id == 42
    assert logs.last_create == {
        "idea_id": 10,
        "author_id": 42,
        "comment": "avance del dia",
        "progress_snapshot": 33.0,
        "status_snapshot": "in_progress",
    }


def test_add_progress_log_rejects_empty_comment() -> None:
    use_case = AddProgressLogUseCase(
        idea_repository=FakeIdeaRepository(_idea()),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(DomainValidationError, match="comment must not be empty"):
        use_case.execute(idea_id=10, data=AddProgressLogInput(comment="   "))


def test_add_progress_log_not_found() -> None:
    use_case = AddProgressLogUseCase(
        idea_repository=FakeIdeaRepository(None),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(NotFoundError, match="idea not found"):
        use_case.execute(idea_id=999, data=AddProgressLogInput(comment="ok"))


def test_add_progress_log_forbidden_for_non_owner_non_admin() -> None:
    use_case = AddProgressLogUseCase(
        idea_repository=FakeIdeaRepository(_idea(owner_id=1)),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=2),
    )
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10, data=AddProgressLogInput(comment="ok"))

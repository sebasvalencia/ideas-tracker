from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord, ProgressLogRecord
from src.app.application.idea.use_cases.list_progress_logs import ListProgressLogsUseCase


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
        now = datetime.now()
        self.items = [
            ProgressLogRecord(
                id=2,
                idea_id=10,
                author_id=42,
                comment="second",
                progress_snapshot=40.0,
                status_snapshot="in_progress",
                created_at=now,
            ),
            ProgressLogRecord(
                id=1,
                idea_id=10,
                author_id=42,
                comment="first",
                progress_snapshot=20.0,
                status_snapshot="in_progress",
                created_at=now - timedelta(minutes=1),
            ),
        ]

    def list_by_idea(self, *, idea_id: int) -> list[ProgressLogRecord]:
        return [item for item in self.items if item.idea_id == idea_id]


def _idea(owner_id: int = 42) -> IdeaRecord:
    now = datetime.now()
    return IdeaRecord(
        id=10,
        owner_id=owner_id,
        title="Idea",
        description="Desc",
        status="in_progress",
        execution_percentage=40.0,
        created_at=now,
        updated_at=now,
        deleted_at=None,
    )


def test_list_progress_logs_success() -> None:
    use_case = ListProgressLogsUseCase(
        idea_repository=FakeIdeaRepository(_idea(owner_id=42)),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    result = use_case.execute(idea_id=10)
    assert [item.id for item in result] == [2, 1]


def test_list_progress_logs_not_found() -> None:
    use_case = ListProgressLogsUseCase(
        idea_repository=FakeIdeaRepository(None),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=42),
    )
    with pytest.raises(NotFoundError, match="idea not found"):
        use_case.execute(idea_id=999)


def test_list_progress_logs_forbidden_for_non_owner_non_admin() -> None:
    use_case = ListProgressLogsUseCase(
        idea_repository=FakeIdeaRepository(_idea(owner_id=1)),
        log_repository=FakeLogRepository(),
        auth_ctx=FakeAuthContext(user_id=2),
    )
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10)

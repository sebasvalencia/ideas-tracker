from __future__ import annotations

from datetime import datetime, timedelta

from src.app.application.idea.dto import ListIdeasInput
from src.app.application.idea.ports import AuthUser, IdeaRecord
from src.app.application.idea.use_cases.list_ideas import ListIdeasUseCase


class FakeAuthContext:
    def current_user(self) -> AuthUser:
        return AuthUser(user_id=42, email="tester@ideas.com", role="user")


class FakeIdeaRepository:
    def __init__(self) -> None:
        base = datetime.now()
        self.items: list[IdeaRecord] = [
            IdeaRecord(
                id=1,
                owner_id=42,
                title="a",
                description="a",
                status="idea",
                execution_percentage=0.0,
                created_at=base - timedelta(minutes=3),
                updated_at=base - timedelta(minutes=3),
                deleted_at=None,
            ),
            IdeaRecord(
                id=2,
                owner_id=42,
                title="b",
                description="b",
                status="in_progress",
                execution_percentage=30.0,
                created_at=base - timedelta(minutes=2),
                updated_at=base - timedelta(minutes=2),
                deleted_at=None,
            ),
            IdeaRecord(
                id=3,
                owner_id=42,
                title="c",
                description="c",
                status="idea",
                execution_percentage=0.0,
                created_at=base - timedelta(minutes=1),
                updated_at=base - timedelta(minutes=1),
                deleted_at=base,
            ),
            IdeaRecord(
                id=4,
                owner_id=7,
                title="other-user",
                description="other-user",
                status="idea",
                execution_percentage=0.0,
                created_at=base,
                updated_at=base,
                deleted_at=None,
            ),
        ]

    def list_active(self, *, owner_id: int, status: str | None, limit: int, offset: int) -> list[IdeaRecord]:
        rows = [item for item in self.items if item.owner_id == owner_id and item.deleted_at is None]
        if status is not None:
            rows = [item for item in rows if item.status == status]
        rows.sort(key=lambda item: item.created_at, reverse=True)
        return rows[offset : offset + limit]


def test_list_ideas_excludes_deleted_and_other_owners() -> None:
    use_case = ListIdeasUseCase(repository=FakeIdeaRepository(), auth_ctx=FakeAuthContext())
    result = use_case.execute(ListIdeasInput())
    assert [item.id for item in result] == [2, 1]


def test_list_ideas_supports_status_filter() -> None:
    use_case = ListIdeasUseCase(repository=FakeIdeaRepository(), auth_ctx=FakeAuthContext())
    result = use_case.execute(ListIdeasInput(status="in_progress"))
    assert [item.id for item in result] == [2]


def test_list_ideas_supports_limit_and_offset() -> None:
    use_case = ListIdeasUseCase(repository=FakeIdeaRepository(), auth_ctx=FakeAuthContext())
    result = use_case.execute(ListIdeasInput(limit=1, offset=1))
    assert [item.id for item in result] == [1]

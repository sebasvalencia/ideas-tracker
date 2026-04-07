from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.dto import UpdateIdeaInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthUser, IdeaRecord, ProgressLogRecord
from src.app.application.idea.use_cases.update_idea import UpdateIdeaUseCase


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

    def update(self, *, idea: IdeaRecord) -> IdeaRecord:
        self._idea = idea
        return idea


class FakeLogRepository:
    def __init__(self) -> None:
        self.items: list[ProgressLogRecord] = []

    def create(
        self,
        *,
        idea_id: int,
        author_id: int,
        comment: str,
        progress_snapshot: float,
        status_snapshot: str,
    ) -> ProgressLogRecord:
        row = ProgressLogRecord(
            id=len(self.items) + 1,
            idea_id=idea_id,
            author_id=author_id,
            comment=comment,
            progress_snapshot=progress_snapshot,
            status_snapshot=status_snapshot,
            created_at=datetime.now(),
        )
        self.items.append(row)
        return row


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


def test_update_success_changes_status_and_progress() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(_idea()), auth_ctx=FakeAuthContext(user_id=42))
    result = use_case.execute(idea_id=10, patch=UpdateIdeaInput(status="in_progress", execution_percentage=25))
    assert result.status == "in_progress"
    assert result.execution_percentage == 25


def test_update_rejects_progress_out_of_range() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(_idea()), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(DomainValidationError, match="execution_percentage must be between 0 and 100"):
        use_case.execute(idea_id=10, patch=UpdateIdeaInput(execution_percentage=120))


def test_update_rejects_completed_without_100_progress() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(_idea()), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(DomainValidationError, match="completed requires execution_percentage=100"):
        use_case.execute(idea_id=10, patch=UpdateIdeaInput(status="completed", execution_percentage=80))


def test_update_rejects_invalid_status() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(_idea()), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(DomainValidationError, match="invalid status"):
        use_case.execute(idea_id=10, patch=UpdateIdeaInput(status="invalid"))


def test_update_not_found() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(None), auth_ctx=FakeAuthContext(user_id=42))
    with pytest.raises(NotFoundError, match="idea not found"):
        use_case.execute(idea_id=999, patch=UpdateIdeaInput(status="idea"))


def test_update_forbidden_for_non_owner_non_admin() -> None:
    use_case = UpdateIdeaUseCase(repository=FakeIdeaRepository(_idea(owner_id=1)), auth_ctx=FakeAuthContext(user_id=2))
    with pytest.raises(ForbiddenError, match="forbidden"):
        use_case.execute(idea_id=10, patch=UpdateIdeaInput(status="in_progress"))


def test_update_creates_system_log_when_status_or_progress_changes() -> None:
    logs = FakeLogRepository()
    use_case = UpdateIdeaUseCase(
        repository=FakeIdeaRepository(_idea()),
        auth_ctx=FakeAuthContext(user_id=42),
        log_repository=logs,
    )
    use_case.execute(idea_id=10, patch=UpdateIdeaInput(status="in_progress", execution_percentage=25))
    assert len(logs.items) == 1
    assert logs.items[0].status_snapshot == "in_progress"
    assert logs.items[0].progress_snapshot == 25


def test_update_does_not_create_system_log_when_only_title_changes() -> None:
    logs = FakeLogRepository()
    use_case = UpdateIdeaUseCase(
        repository=FakeIdeaRepository(_idea()),
        auth_ctx=FakeAuthContext(user_id=42),
        log_repository=logs,
    )
    use_case.execute(idea_id=10, patch=UpdateIdeaInput(title="Nuevo titulo"))
    assert logs.items == []

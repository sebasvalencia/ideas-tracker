from __future__ import annotations

from datetime import datetime

import pytest

from src.app.application.idea.dto import CreateIdeaInput
from src.app.application.idea.errors import DomainValidationError
from src.app.application.idea.ports import AuthUser, IdeaRecord
from src.app.application.idea.use_cases.create_idea import CreateIdeaUseCase


class FakeAuthContext:
    def current_user(self) -> AuthUser:
        return AuthUser(user_id=42, email="tester@ideas.com", role="user")


class FakeIdeaRepository:
    def __init__(self) -> None:
        self.last_create: dict | None = None

    def create(self, *, owner_id: int, title: str, description: str) -> IdeaRecord:
        self.last_create = {
            "owner_id": owner_id,
            "title": title,
            "description": description,
        }
        now = datetime.now()
        return IdeaRecord(
            id=1,
            owner_id=owner_id,
            title=title,
            description=description,
            status="idea",
            execution_percentage=0.0,
            created_at=now,
            updated_at=now,
            deleted_at=None,
        )


def test_create_idea_sets_initial_state_progress_and_owner() -> None:
    repo = FakeIdeaRepository()
    use_case = CreateIdeaUseCase(repository=repo, auth_ctx=FakeAuthContext())

    result = use_case.execute(CreateIdeaInput(title="  My idea  ", description="  Details  "))

    assert result.owner_id == 42
    assert result.status == "idea"
    assert result.execution_percentage == 0.0
    assert repo.last_create == {
        "owner_id": 42,
        "title": "My idea",
        "description": "Details",
    }


def test_create_idea_rejects_empty_title() -> None:
    use_case = CreateIdeaUseCase(repository=FakeIdeaRepository(), auth_ctx=FakeAuthContext())
    with pytest.raises(DomainValidationError, match="title must not be empty"):
        use_case.execute(CreateIdeaInput(title="   ", description="valid"))


def test_create_idea_rejects_empty_description() -> None:
    use_case = CreateIdeaUseCase(repository=FakeIdeaRepository(), auth_ctx=FakeAuthContext())
    with pytest.raises(DomainValidationError, match="description must not be empty"):
        use_case.execute(CreateIdeaInput(title="valid", description="   "))

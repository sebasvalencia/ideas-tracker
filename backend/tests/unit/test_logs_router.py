from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.main import app

FAKE_CLAIMS = {"sub": "1", "email": "u@test.com", "roles": ["user"]}
_NOW = datetime(2024, 1, 1, 12, 0, 0)


class _Log:
    def __init__(self) -> None:
        self.id = 1
        self.idea_id = 1
        self.author_id = 1
        self.comment = "Progress made"
        self.progress_snapshot = 25.0
        self.status_snapshot = "in_progress"
        self.created_at = _NOW


@pytest.fixture(autouse=True)
def _inject_user():
    app.dependency_overrides[get_current_user] = lambda: FAKE_CLAIMS
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_add_progress_log_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            return _Log()

    monkeypatch.setattr(logs_router, "get_add_progress_log_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/logs", json={"comment": "Progress made"})
    assert resp.status_code == 201
    assert resp.json()["comment"] == "Progress made"


def test_add_progress_log_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise NotFoundError("idea not found")

    monkeypatch.setattr(logs_router, "get_add_progress_log_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/99/logs", json={"comment": "Progress"})
    assert resp.status_code == 404


def test_add_progress_log_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(logs_router, "get_add_progress_log_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/logs", json={"comment": "Progress"})
    assert resp.status_code == 403


def test_add_progress_log_validation_error(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise DomainValidationError("comment cannot be empty")

    monkeypatch.setattr(logs_router, "get_add_progress_log_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/logs", json={"comment": ""})
    assert resp.status_code == 422


def test_list_progress_logs_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            return [_Log()]

    monkeypatch.setattr(logs_router, "get_list_progress_logs_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1/logs")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["comment"] == "Progress made"


def test_list_progress_logs_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("idea not found")

    monkeypatch.setattr(logs_router, "get_list_progress_logs_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/99/logs")
    assert resp.status_code == 404


def test_list_progress_logs_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import logs_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(logs_router, "get_list_progress_logs_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1/logs")
    assert resp.status_code == 403

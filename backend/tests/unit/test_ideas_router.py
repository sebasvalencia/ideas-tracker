from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.main import app

FAKE_CLAIMS = {"sub": "1", "email": "u@test.com", "roles": ["user"]}
_NOW = datetime(2024, 1, 1, 12, 0, 0)


class _Idea:
    def __init__(self, status: str = "draft") -> None:
        self.id = 1
        self.owner_id = 1
        self.title = "Test Idea"
        self.description = "A description"
        self.status = status
        self.execution_percentage = 0.0
        self.created_at = _NOW
        self.updated_at = _NOW
        self.deleted_at = None


@pytest.fixture(autouse=True)
def _inject_user():
    app.dependency_overrides[get_current_user] = lambda: FAKE_CLAIMS
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_create_idea_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, data):  # noqa: ANN001
            return _Idea()

    monkeypatch.setattr(ideas_router, "get_create_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas", json={"title": "Test", "description": "Desc"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "Test Idea"


def test_create_idea_validation_error(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, data):  # noqa: ANN001
            raise DomainValidationError("title too short")

    monkeypatch.setattr(ideas_router, "get_create_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas", json={"title": "", "description": "Desc"})
    assert resp.status_code == 422


def test_list_ideas_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, data):  # noqa: ANN001
            return [_Idea()]

    monkeypatch.setattr(ideas_router, "get_list_ideas_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas")
    assert resp.status_code == 200
    assert resp.json()[0]["title"] == "Test Idea"


def test_get_idea_detail_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Idea()

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1")
    assert resp.status_code == 200


def test_get_idea_detail_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("idea not found")

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/99")
    assert resp.status_code == 404


def test_get_idea_detail_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1")
    assert resp.status_code == 403


def test_update_idea_success_with_completion(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _DetailUC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Idea(status="draft")

    class _UpdateUC:
        def execute(self, idea_id, patch):  # noqa: ANN001
            return _Idea(status="completed")

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _DetailUC())
    monkeypatch.setattr(ideas_router, "get_update_idea_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1", json={"status": "completed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_update_idea_no_transition(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _DetailUC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Idea(status="draft")

    class _UpdateUC:
        def execute(self, idea_id, patch):  # noqa: ANN001
            return _Idea(status="in_progress")

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _DetailUC())
    monkeypatch.setattr(ideas_router, "get_update_idea_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1", json={"status": "in_progress"})
    assert resp.status_code == 200


def test_update_idea_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _DetailUC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("idea not found")

    class _UpdateUC:
        def execute(self, idea_id, patch):  # noqa: ANN001
            return _Idea()

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _DetailUC())
    monkeypatch.setattr(ideas_router, "get_update_idea_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/99", json={"status": "in_progress"})
    assert resp.status_code == 404


def test_update_idea_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _DetailUC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    class _UpdateUC:
        def execute(self, idea_id, patch):  # noqa: ANN001
            return _Idea()

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _DetailUC())
    monkeypatch.setattr(ideas_router, "get_update_idea_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1", json={"status": "in_progress"})
    assert resp.status_code == 403


def test_update_idea_validation_error(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _DetailUC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Idea()

    class _UpdateUC:
        def execute(self, idea_id, patch):  # noqa: ANN001
            raise DomainValidationError("invalid status")

    monkeypatch.setattr(ideas_router, "get_idea_detail_use_case_for_claims", lambda u: _DetailUC())
    monkeypatch.setattr(ideas_router, "get_update_idea_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1", json={"status": "bad"})
    assert resp.status_code == 422


def test_delete_idea_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            return None

    monkeypatch.setattr(ideas_router, "get_delete_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.delete("/api/v1/ideas/1")
    assert resp.status_code == 204


def test_delete_idea_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("not found")

    monkeypatch.setattr(ideas_router, "get_delete_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.delete("/api/v1/ideas/99")
    assert resp.status_code == 404


def test_delete_idea_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ideas_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(ideas_router, "get_delete_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.delete("/api/v1/ideas/1")
    assert resp.status_code == 403

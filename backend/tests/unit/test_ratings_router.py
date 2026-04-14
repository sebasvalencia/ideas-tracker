from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.main import app

FAKE_CLAIMS = {"sub": "1", "email": "u@test.com", "roles": ["user"]}
_NOW = datetime(2024, 1, 1, 12, 0, 0)


class _Rating:
    def __init__(self) -> None:
        self.id = 1
        self.idea_id = 1
        self.rating = 4
        self.summary = "Great idea"
        self.created_at = _NOW


@pytest.fixture(autouse=True)
def _inject_user():
    app.dependency_overrides[get_current_user] = lambda: FAKE_CLAIMS
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_rate_idea_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            return _Rating()

    monkeypatch.setattr(ratings_router, "get_rate_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/rating", json={"rating": 4, "summary": "Great"})
    assert resp.status_code == 201
    assert resp.json()["rating"] == 4


def test_rate_idea_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise NotFoundError("idea not found")

    monkeypatch.setattr(ratings_router, "get_rate_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/99/rating", json={"rating": 4})
    assert resp.status_code == 404


def test_rate_idea_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(ratings_router, "get_rate_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/rating", json={"rating": 4})
    assert resp.status_code == 403


def test_rate_idea_validation_error(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id, data):  # noqa: ANN001
            raise DomainValidationError("rating out of range")

    monkeypatch.setattr(ratings_router, "get_rate_idea_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.post("/api/v1/ideas/1/rating", json={"rating": 99})
    assert resp.status_code == 422


def test_update_idea_rating_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _ReadUC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Rating()

    class _UpdateUC:
        def execute(self, idea_id, data):  # noqa: ANN001
            return _Rating()

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _ReadUC())
    monkeypatch.setattr(ratings_router, "get_update_idea_rating_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1/rating", json={"rating": 5})
    assert resp.status_code == 200
    assert resp.json()["rating"] == 4


def test_update_idea_rating_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _ReadUC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("rating not found")

    class _UpdateUC:
        def execute(self, idea_id, data):  # noqa: ANN001
            return _Rating()

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _ReadUC())
    monkeypatch.setattr(ratings_router, "get_update_idea_rating_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/99/rating", json={"rating": 5})
    assert resp.status_code == 404


def test_update_idea_rating_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _ReadUC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    class _UpdateUC:
        def execute(self, idea_id, data):  # noqa: ANN001
            return _Rating()

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _ReadUC())
    monkeypatch.setattr(ratings_router, "get_update_idea_rating_use_case_for_claims", lambda u: _UpdateUC())
    with TestClient(app) as client:
        resp = client.patch("/api/v1/ideas/1/rating", json={"rating": 5})
    assert resp.status_code == 403


def test_get_idea_rating_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            return _Rating()

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1/rating")
    assert resp.status_code == 200
    assert resp.json()["rating"] == 4


def test_get_idea_rating_not_found(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise NotFoundError("rating not found")

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/99/rating")
    assert resp.status_code == 404


def test_get_idea_rating_forbidden(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import ratings_router

    class _UC:
        def execute(self, idea_id):  # noqa: ANN001
            raise ForbiddenError("not your idea")

    monkeypatch.setattr(ratings_router, "get_idea_rating_use_case_for_claims", lambda u: _UC())
    with TestClient(app) as client:
        resp = client.get("/api/v1/ideas/1/rating")
    assert resp.status_code == 403

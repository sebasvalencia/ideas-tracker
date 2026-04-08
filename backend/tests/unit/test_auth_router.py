from fastapi.testclient import TestClient

from src.app.application.auth.errors import AuthError
from src.main import app


class _LoginUseCaseOk:
    def execute(self, _data):  # noqa: ANN001
        class _Result:
            def __init__(self):
                self.access_token = "token"
                self.refresh_token = "refresh"
                self.token_type = "bearer"

        return _Result()


class _LoginUseCaseFail:
    def execute(self, _data):  # noqa: ANN001
        raise AuthError("invalid credentials")


class _RefreshUseCaseOk:
    def execute(self, _data):  # noqa: ANN001
        class _Result:
            def __init__(self):
                self.access_token = "new-token"
                self.refresh_token = "new-refresh"
                self.token_type = "bearer"

        return _Result()


class _RefreshUseCaseFail:
    def execute(self, _data):  # noqa: ANN001
        raise AuthError("invalid refresh token")


def test_auth_login_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import auth_router

    monkeypatch.setattr(auth_router, "get_login_use_case", lambda: _LoginUseCaseOk())
    with TestClient(app) as client:
        response = client.post("/api/v1/auth/login", json={"email": "admin@ideas.com", "password": "secret"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"] == "token"
    assert payload["token_type"] == "bearer"


def test_auth_login_invalid_credentials(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import auth_router

    monkeypatch.setattr(auth_router, "get_login_use_case", lambda: _LoginUseCaseFail())
    with TestClient(app) as client:
        response = client.post("/api/v1/auth/login", json={"email": "admin@ideas.com", "password": "wrong"})

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"


def test_auth_refresh_success(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import auth_router

    monkeypatch.setattr(auth_router, "get_refresh_token_use_case", lambda: _RefreshUseCaseOk())
    with TestClient(app) as client:
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": "refresh"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["access_token"] == "new-token"
    assert payload["token_type"] == "bearer"


def test_auth_refresh_invalid_token(monkeypatch) -> None:
    from src.app.adapters.inbound.rest.routers import auth_router

    monkeypatch.setattr(auth_router, "get_refresh_token_use_case", lambda: _RefreshUseCaseFail())
    with TestClient(app) as client:
        response = client.post("/api/v1/auth/refresh", json={"refresh_token": "invalid"})

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid refresh token"

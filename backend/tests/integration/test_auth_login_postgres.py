from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from scripts.seed import main as seed_main
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal
from src.main import app

LOGIN_URL = "/api/v1/auth/login"
ADMIN_EMAIL = "admin@ideas.com"
ADMIN_PASSWORD = "ChangeMe123!"


@pytest.fixture(scope="module")
def client() -> TestClient:
    # Ensure DB is reachable and baseline data exists.
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Postgres not available for integration test: {exc}")

    seed_main()
    with TestClient(app) as c:
        yield c


def _login(client: TestClient, password: str):
    return client.post(
        LOGIN_URL,
        json={"email": ADMIN_EMAIL, "password": password},
    )


def test_login_success_real_postgres(client: TestClient) -> None:
    response = _login(client, ADMIN_PASSWORD)
    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["refresh_token"]


def test_login_invalid_password_real_postgres(client: TestClient) -> None:
    response = _login(client, "wrong-password")
    assert response.status_code == 401

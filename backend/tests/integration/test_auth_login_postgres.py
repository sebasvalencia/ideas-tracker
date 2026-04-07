from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from scripts.seed import main as seed_main
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal
from src.main import app

LOGIN_URL = "/api/v1/auth/login"
IDEAS_URL = "/api/v1/ideas"
ADMIN_EMAIL = "admin@ideas.com"
ADMIN_PASSWORD = "ChangeMe123!"


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    # Ensure DB is reachable and baseline data exists.
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Postgres not available for integration test: {exc}")

    seed_main()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def access_token(client: TestClient) -> str:
    response = _login(client, ADMIN_PASSWORD)
    assert response.status_code == 200
    return response.json()["access_token"]


def _login(client: TestClient, password: str):
    return client.post(
        LOGIN_URL,
        json={"email": ADMIN_EMAIL, "password": password},
    )


def _create_idea(client: TestClient, access_token: str):
    return client.post(
        IDEAS_URL,
        json={"title": "Secure idea", "description": "Protected endpoint test"},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _update_idea(client: TestClient, access_token: str, idea_id: int, payload: dict):
    return client.patch(
        f"{IDEAS_URL}/{idea_id}",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _delete_idea(client: TestClient, access_token: str, idea_id: int):
    return client.delete(
        f"{IDEAS_URL}/{idea_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _add_progress_log(client: TestClient, access_token: str, idea_id: int, comment: str):
    return client.post(
        f"{IDEAS_URL}/{idea_id}/logs",
        json={"comment": comment},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _rate_idea(client: TestClient, access_token: str, idea_id: int, payload: dict):
    return client.post(
        f"{IDEAS_URL}/{idea_id}/rating",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _update_idea_rating(client: TestClient, access_token: str, idea_id: int, payload: dict):
    return client.patch(
        f"{IDEAS_URL}/{idea_id}/rating",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def _get_idea_rating(client: TestClient, access_token: str, idea_id: int):
    return client.get(
        f"{IDEAS_URL}/{idea_id}/rating",
        headers={"Authorization": f"Bearer {access_token}"},
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


def test_create_idea_requires_token(client: TestClient) -> None:
    response = client.post(
        IDEAS_URL,
        json={"title": "No token", "description": "Should fail"},
    )
    assert response.status_code in (401, 403)


def test_create_idea_with_token_uses_authenticated_owner(client: TestClient, access_token: str) -> None:
    response = _create_idea(client, access_token)
    assert response.status_code == 201

    payload = response.json()
    assert payload["owner_id"] > 0
    assert payload["status"] == "idea"
    assert payload["execution_percentage"] == 0.0


def test_list_ideas_requires_token(client: TestClient) -> None:
    response = client.get(IDEAS_URL)
    assert response.status_code in (401, 403)


def test_list_ideas_with_token_returns_paginated_items(client: TestClient, access_token: str) -> None:
    _create_idea(client, access_token)
    _create_idea(client, access_token)

    response = client.get(
        IDEAS_URL,
        params={"limit": 1, "offset": 0},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 1
    assert payload[0]["owner_id"] > 0


def test_get_idea_detail_with_token_returns_item(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = client.get(
        f"{IDEAS_URL}/{idea_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == idea_id
    assert payload["owner_id"] > 0


def test_get_idea_detail_returns_404_for_missing_id(client: TestClient, access_token: str) -> None:
    response = client.get(
        f"{IDEAS_URL}/99999999",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404


def test_update_idea_with_token_success(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = _update_idea(
        client,
        access_token,
        idea_id,
        {"status": "in_progress", "execution_percentage": 40},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "in_progress"
    assert payload["execution_percentage"] == 40


def test_update_idea_rejects_out_of_range_progress(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = _update_idea(client, access_token, idea_id, {"execution_percentage": 120})
    assert response.status_code == 422


def test_update_idea_rejects_completed_without_100(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = _update_idea(
        client,
        access_token,
        idea_id,
        {"status": "completed", "execution_percentage": 80},
    )
    assert response.status_code == 422


def test_delete_idea_soft_delete_hides_from_detail_and_list(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    delete_response = _delete_idea(client, access_token, idea_id)
    assert delete_response.status_code == 204

    detail_response = client.get(
        f"{IDEAS_URL}/{idea_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert detail_response.status_code == 404

    list_response = client.get(
        IDEAS_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert list_response.status_code == 200
    ids = [row["id"] for row in list_response.json()]
    assert idea_id not in ids


def test_add_progress_log_with_token_uses_snapshot_and_author(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    _update_idea(client, access_token, idea_id, {"status": "in_progress", "execution_percentage": 45})
    response = _add_progress_log(client, access_token, idea_id, "avance funcional")

    assert response.status_code == 201
    payload = response.json()
    assert payload["idea_id"] == idea_id
    assert payload["author_id"] > 0
    assert payload["status_snapshot"] == "in_progress"
    assert payload["progress_snapshot"] == 45


def test_add_progress_log_rejects_empty_comment(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = _add_progress_log(client, access_token, idea_id, "   ")
    assert response.status_code == 422


def test_list_progress_logs_returns_desc_order(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    _update_idea(client, access_token, idea_id, {"status": "in_progress", "execution_percentage": 10})
    first = _add_progress_log(client, access_token, idea_id, "first log")
    assert first.status_code == 201

    _update_idea(client, access_token, idea_id, {"execution_percentage": 20})
    second = _add_progress_log(client, access_token, idea_id, "second log")
    assert second.status_code == 201

    response = client.get(
        f"{IDEAS_URL}/{idea_id}/logs",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    comments = [row["comment"] for row in payload]
    assert "first log" in comments
    assert "second log" in comments
    assert comments.index("second log") < comments.index("first log")


def test_rate_idea_requires_completed_status(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    response = _rate_idea(client, access_token, idea_id, {"rating": 8, "summary": "ok"})
    assert response.status_code == 422


def test_rate_update_get_idea_rating_flow(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    _update_idea(client, access_token, idea_id, {"status": "completed", "execution_percentage": 100})

    rate_response = _rate_idea(client, access_token, idea_id, {"rating": 7, "summary": "bien"})
    assert rate_response.status_code == 201
    assert rate_response.json()["rating"] == 7

    update_response = _update_idea_rating(client, access_token, idea_id, {"rating": 9, "summary": "excelente"})
    assert update_response.status_code == 200
    assert update_response.json()["rating"] == 9

    get_response = _get_idea_rating(client, access_token, idea_id)
    assert get_response.status_code == 200
    payload = get_response.json()
    assert payload["rating"] == 9
    assert payload["summary"] == "excelente"


def test_rate_idea_rejects_out_of_range(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]
    _update_idea(client, access_token, idea_id, {"status": "completed", "execution_percentage": 100})

    response = _rate_idea(client, access_token, idea_id, {"rating": 11})
    assert response.status_code == 422


def test_update_idea_creates_system_log_automatically(client: TestClient, access_token: str) -> None:
    create_response = _create_idea(client, access_token)
    assert create_response.status_code == 201
    idea_id = create_response.json()["id"]

    update_response = _update_idea(
        client,
        access_token,
        idea_id,
        {"status": "in_progress", "execution_percentage": 30},
    )
    assert update_response.status_code == 200

    logs_response = client.get(
        f"{IDEAS_URL}/{idea_id}/logs",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert logs_response.status_code == 200
    comments = [row["comment"] for row in logs_response.json()]
    assert any(comment.startswith("[system] state/progress changed") for comment in comments)

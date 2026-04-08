from __future__ import annotations

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/ideas.feature")


@given(parsers.parse('I am authenticated as "{email}" with password "{password}"'))
def authenticate_user(bdd_client, bdd_context: dict, email: str, password: str) -> None:
    response = bdd_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    bdd_context["access_token"] = response.json()["access_token"]


@when(parsers.parse('I create an idea with title "{title}" and description "{description}"'))
def create_idea(bdd_client, bdd_context: dict, title: str, description: str) -> None:
    response = bdd_client.post(
        "/api/v1/ideas",
        json={"title": title, "description": description},
        headers={"Authorization": f"Bearer {bdd_context['access_token']}"},
    )
    bdd_context["response"] = response
    if response.status_code == 201:
        bdd_context["created_idea"] = response.json()


@then("the created idea should have owner and status")
def created_idea_shape(bdd_context: dict) -> None:
    payload = bdd_context["created_idea"]
    assert payload["owner_id"] > 0
    assert payload["status"] in {"idea", "in_progress", "completed"}


@when("I list my ideas")
def list_ideas(bdd_client, bdd_context: dict) -> None:
    response = bdd_client.get(
        "/api/v1/ideas",
        headers={"Authorization": f"Bearer {bdd_context['access_token']}"},
    )
    bdd_context["response"] = response
    if response.status_code == 200:
        bdd_context["ideas"] = response.json()


@then(parsers.parse("the response status should be {status:d}"))
def response_status(bdd_context: dict, status: int) -> None:
    assert bdd_context["response"].status_code == status


@then(parsers.parse('the ideas list should contain title "{title}"'))
def ideas_contains_title(bdd_context: dict, title: str) -> None:
    titles = [row["title"] for row in bdd_context["ideas"]]
    assert title in titles

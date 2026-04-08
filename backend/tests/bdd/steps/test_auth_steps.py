from __future__ import annotations

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/auth.feature")


@given(parsers.parse('an active user with email "{email}" and password "{password}"'))
def user_credentials(bdd_context: dict, email: str, password: str) -> None:
    bdd_context["email"] = email
    bdd_context["password"] = password


@when(parsers.parse('I submit POST "{path}" with those credentials'))
def submit_login(bdd_client, bdd_context: dict, path: str) -> None:
    response = bdd_client.post(
        path,
        json={
            "email": bdd_context["email"],
            "password": bdd_context["password"],
        },
    )
    bdd_context["response"] = response


@then(parsers.parse("the response status should be {status:d}"))
def response_status(bdd_context: dict, status: int) -> None:
    assert bdd_context["response"].status_code == status


@then(parsers.parse('the response should include "{field_name}"'))
def response_contains_field(bdd_context: dict, field_name: str) -> None:
    payload = bdd_context["response"].json()
    assert payload.get(field_name)

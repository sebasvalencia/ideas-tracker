import pytest
from fastapi import HTTPException, status

from src.app.adapters.inbound.rest.auth_dependencies import require_roles


def test_require_roles_allows_matching_role() -> None:
    checker = require_roles("admin")
    admin_user = {"roles": ["admin"]}
    assert checker(admin_user) == admin_user


@pytest.mark.parametrize("roles", [["user"], ["viewer"], []])
def test_require_roles_forbidden_when_missing(roles: list[str]) -> None:
    checker = require_roles("admin")
    with pytest.raises(HTTPException) as exc:
        checker({"roles": roles})
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
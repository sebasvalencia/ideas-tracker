import pytest

from src.app.adapters.outbound.security.auth_context import JwtAuthContext


def test_current_user_with_roles() -> None:
    ctx = JwtAuthContext({"sub": "42", "email": "user@test.com", "roles": ["admin"]})
    user = ctx.current_user()
    assert user.user_id == 42
    assert user.email == "user@test.com"
    assert user.role == "admin"


def test_current_user_no_roles_defaults_to_user() -> None:
    ctx = JwtAuthContext({"sub": "7", "email": "other@test.com", "roles": []})
    user = ctx.current_user()
    assert user.user_id == 7
    assert user.role == "user"


def test_current_user_missing_roles_key() -> None:
    ctx = JwtAuthContext({"sub": "3", "email": "x@test.com"})
    user = ctx.current_user()
    assert user.role == "user"


def test_current_user_missing_sub_raises() -> None:
    ctx = JwtAuthContext({"email": "x@test.com", "roles": ["user"]})
    with pytest.raises(ValueError, match="token missing subject"):
        ctx.current_user()

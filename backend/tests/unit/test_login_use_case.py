import pytest

from src.app.application.auth.dto import LoginInput
from src.app.application.auth.errors import AuthError
from src.app.application.auth.use_cases.login import LoginUseCase
from tests.unit.fakes import FakeHasher, FakeTokenService, FakeUser, FakeUsersRepo


def test_login_success() -> None:
    uc = LoginUseCase(FakeUsersRepo(FakeUser()), FakeHasher(verify_result=True), FakeTokenService())
    result = uc.execute(LoginInput(email="user@test.com", password="Secret123!"))
    assert result.access_token == "token-123"
    assert result.refresh_token == "refresh-123"


def test_login_invalid_password() -> None:
    uc = LoginUseCase(FakeUsersRepo(FakeUser()), FakeHasher(verify_result=False), FakeTokenService())
    with pytest.raises(AuthError):
        uc.execute(LoginInput(email="user@test.com", password="bad"))


def test_login_rejects_inactive_user() -> None:
    inactive_user = FakeUser(is_active=False)
    uc = LoginUseCase(FakeUsersRepo(inactive_user), FakeHasher(verify_result=True), FakeTokenService())
    with pytest.raises(AuthError):
        uc.execute(LoginInput(email="user@test.com", password="Secret123!"))

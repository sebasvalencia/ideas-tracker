import pytest

from src.app.application.auth.dto import RefreshTokenInput
from src.app.application.auth.errors import AuthError
from src.app.application.auth.use_cases.refresh_token import RefreshTokenUseCase
from tests.unit.fakes import FakeRefreshTokens


def test_refresh_success() -> None:
    uc = RefreshTokenUseCase(tokens=FakeRefreshTokens())
    result = uc.execute(RefreshTokenInput(refresh_token="r1"))
    assert result.access_token == "new-access"
    assert result.refresh_token == "new-refresh"


def test_refresh_rejects_non_refresh_token() -> None:
    uc = RefreshTokenUseCase(tokens=FakeRefreshTokens(payload={"type": "access"}))
    with pytest.raises(AuthError):
        uc.execute(RefreshTokenInput(refresh_token="bad"))


def test_refresh_rejects_missing_subject() -> None:
    uc = RefreshTokenUseCase(tokens=FakeRefreshTokens(payload={"type": "refresh", "email": "u@test.com"}))
    with pytest.raises(AuthError):
        uc.execute(RefreshTokenInput(refresh_token="bad"))

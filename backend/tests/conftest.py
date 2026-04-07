import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.unit.fakes import FakeRefreshTokens, FakeTokenService, FakeUser, FakeUsersRepo  # noqa: E402


@pytest.fixture
def fake_user() -> FakeUser:
    return FakeUser()


@pytest.fixture
def users_repo(fake_user: FakeUser) -> FakeUsersRepo:
    return FakeUsersRepo(fake_user)


@pytest.fixture
def token_service() -> FakeTokenService:
    return FakeTokenService()


@pytest.fixture
def refresh_tokens() -> FakeRefreshTokens:
    return FakeRefreshTokens()

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FakeUser:
    id: int = 1
    email: str = "user@test.com"
    password_hash: str = "hashed-password"
    roles: list[str] = field(default_factory=lambda: ["user"])
    is_active: bool = True


class FakeUsersRepo:
    def __init__(self, user: FakeUser | None) -> None:
        self._user = user

    def get_by_email(self, email: str):
        _ = email
        return self._user


class FakeHasher:
    def __init__(self, verify_result: bool = True) -> None:
        self._verify_result = verify_result

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        _ = (raw_password, hashed_password)
        return self._verify_result


class FakeTokenService:
    def create_access_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        _ = (sub, email, roles)
        return "token-123"

    def create_refresh_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        _ = (sub, email, roles)
        return "refresh-123"


class FakeRefreshTokens:
    def __init__(self, payload: dict | None = None) -> None:
        self._payload = payload or {
            "sub": "1",
            "email": "u@test.com",
            "roles": ["user"],
            "type": "refresh",
        }

    def decode_token(self, token: str) -> dict:
        _ = token
        return self._payload

    def create_access_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        _ = (sub, email, roles)
        return "new-access"

    def create_refresh_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        _ = (sub, email, roles)
        return "new-refresh"

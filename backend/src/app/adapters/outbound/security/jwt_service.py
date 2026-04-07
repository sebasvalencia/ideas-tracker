from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt


class JwtService:
    def __init__(
        self,
        *,
        secret: str,
        algorithm: str = "HS256",
        expire_minutes: int = 30,
        refresh_expire_minutes: int = 60 * 24 * 7,
    ) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes
        self._refresh_expire_minutes = refresh_expire_minutes

    def create_access_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": sub,
            "email": email,
            "roles": roles,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._expire_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def create_refresh_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": sub,
            "email": email,
            "roles": roles,
            "type": "refresh",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=self._refresh_expire_minutes)).timestamp()),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except JWTError as exc:
            raise ValueError("invalid token") from exc
        return payload


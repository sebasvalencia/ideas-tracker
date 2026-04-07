from typing import Protocol

class UserRecord(Protocol):
    id: int
    email: str
    password_hash: str
    roles: list[str]
    is_active: bool

class UserQueryPort(Protocol):
    def get_by_email(self, email: str) -> UserRecord | None:
        ...

class TokenServicePort(Protocol):
    def create_access_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        ...

    def create_refresh_token(self, *, sub: str, email: str, roles: list[str]) -> str:
        ...

    def decode_token(self, token: str) -> dict:
        ...
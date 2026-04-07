from dataclasses import dataclass

@dataclass(frozen=True)
class LoginInput:
    email: str
    password: str


@dataclass(frozen=True)
class TokenOutput:
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


@dataclass(frozen=True)
class RefreshTokenInput:
    refresh_token: str
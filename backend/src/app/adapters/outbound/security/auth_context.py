from src.app.application.idea.ports import AuthUser


class JwtAuthContext:
    def __init__(self, claims: dict) -> None:
        self._claims = claims

    def current_user(self) -> AuthUser:
        sub = self._claims.get("sub")
        if sub is None:
            raise ValueError("token missing subject")

        roles = self._claims.get("roles", [])
        role = roles[0] if roles else "user"
        return AuthUser(
            user_id=int(sub),
            email=str(self._claims.get("email", "")),
            role=role,
        )
from src.app.application.idea.ports import AuthUser


class StaticAuthContext:
    def current_user(self) -> AuthUser:
        # Stub temporal para F1-04; se reemplaza por JWT en Fase 3.
        return AuthUser(user_id=1, email="dev@localhost.com", role="user")
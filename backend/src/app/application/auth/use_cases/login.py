from src.app.application.auth.dto import LoginInput, TokenOutput
from src.app.application.auth.errors import AuthError
from src.app.application.auth.ports import TokenServicePort, UserQueryPort
from src.app.application.security.ports import PasswordHasherPort

class LoginUseCase:
    def __init__( self, users: UserQueryPort, hasher: PasswordHasherPort, tokens: TokenServicePort) -> None:
        self._users = users
        self._hasher = hasher
        self._tokens = tokens
    
    def execute(self, data: LoginInput) -> TokenOutput:
        user = self._users.get_by_email(data.email.strip().lower())
        if not user or not user.is_active:
            raise AuthError("invalid credentials")
        if not self._hasher.verify(data.password, user.password_hash):
            raise AuthError("invalid credentials")
        token = self._tokens.create_access_token(
            sub=str(user.id),
            email=user.email,
            roles=user.roles,
        )
        refresh_token = self._tokens.create_refresh_token(
            sub=str(user.id),
            email=user.email,
            roles=user.roles,
        )
        return TokenOutput(access_token=token, refresh_token=refresh_token)
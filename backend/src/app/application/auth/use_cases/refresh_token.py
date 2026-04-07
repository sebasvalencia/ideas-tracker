from src.app.application.auth.dto import RefreshTokenInput, TokenOutput
from src.app.application.auth.errors import AuthError
from src.app.application.auth.ports import TokenServicePort


class RefreshTokenUseCase:
    def __init__(self, tokens: TokenServicePort) -> None:
        self._tokens = tokens

    def execute(self, data: RefreshTokenInput) -> TokenOutput:
        payload = self._tokens.decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthError("invalid refresh token")

        sub = str(payload.get("sub", ""))
        email = str(payload.get("email", ""))
        roles = payload.get("roles", [])

        if not sub or not email:
            raise AuthError("invalid refresh token")

        access_token = self._tokens.create_access_token(sub=sub, email=email, roles=roles)
        refresh_token = self._tokens.create_refresh_token(sub=sub, email=email, roles=roles)
        return TokenOutput(access_token=access_token, refresh_token=refresh_token)

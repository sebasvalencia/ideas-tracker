from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.app.bootstrap.container import get_token_service

bearer = HTTPBearer(auto_error=True)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    token_service = get_token_service()
    try:
        return token_service.decode_token(creds.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token") from exc

def require_roles(*allowed_roles: str):
    def checker(user: dict = Depends(get_current_user)) -> dict:
        roles = set(user.get("roles", []))
        if not roles.intersection(set(allowed_roles)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
        return user
    return checker
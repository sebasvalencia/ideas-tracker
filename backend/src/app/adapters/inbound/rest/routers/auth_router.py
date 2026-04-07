from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, EmailStr

from src.app.application.auth.dto import LoginInput, RefreshTokenInput
from src.app.application.auth.errors import AuthError
from src.app.adapters.inbound.rest.rate_limiter import LOGIN_RATE_LIMIT, limiter
from src.app.bootstrap.container import get_login_use_case, get_refresh_token_use_case


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/login")
@limiter.limit(LOGIN_RATE_LIMIT)
def login(request: Request, payload: LoginRequest):
    use_case = get_login_use_case()
    try:
        return use_case.execute(LoginInput(email=payload.email, password=payload.password)).__dict__
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest):
    use_case = get_refresh_token_use_case()
    try:
        return use_case.execute(RefreshTokenInput(refresh_token=payload.refresh_token)).__dict__
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
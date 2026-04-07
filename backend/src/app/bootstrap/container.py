from src.app.adapters.outbound.persistence.in_memory.idea_repository import InMemoryIdeaRepository
from src.app.adapters.outbound.persistence.sqlalchemy.repositories.user_query import SqlAlchemyUserQuery
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal
from src.app.adapters.outbound.security.auth_context import StaticAuthContext
from src.app.adapters.outbound.security.jwt_service import JwtService
from src.app.adapters.outbound.security.password_hasher import PasswordHasher
from src.app.application.auth.use_cases.login import LoginUseCase
from src.app.application.auth.use_cases.refresh_token import RefreshTokenUseCase
from src.app.application.idea.use_cases.create_idea import CreateIdeaUseCase
from src.app.bootstrap.settings import settings

_repo = InMemoryIdeaRepository()
_auth = StaticAuthContext()
_password_hasher = PasswordHasher()
_users_query = SqlAlchemyUserQuery(SessionLocal)
_token_service = JwtService(
    secret=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    expire_minutes=settings.JWT_EXPIRE_MINUTES,
    refresh_expire_minutes=settings.JWT_REFRESH_EXPIRE_MINUTES,
)

def get_create_idea_use_case() -> CreateIdeaUseCase:
    return CreateIdeaUseCase(repository=_repo, auth_ctx=_auth)


def get_token_service() -> JwtService:
    return _token_service


def get_login_use_case() -> LoginUseCase:
    return LoginUseCase(users=_users_query, hasher=_password_hasher, tokens=_token_service)


def get_refresh_token_use_case() -> RefreshTokenUseCase:
    return RefreshTokenUseCase(tokens=_token_service)
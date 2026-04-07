from typing import cast

from src.app.adapters.outbound.persistence.sqlalchemy.repositories.idea_repository import SqlAlchemyIdeaRepository
from src.app.adapters.outbound.persistence.sqlalchemy.repositories.progress_log_repository import SqlAlchemyProgressLogRepository
from src.app.adapters.outbound.persistence.sqlalchemy.repositories.rating_repository import SqlAlchemyRatingRepository
from src.app.adapters.outbound.persistence.sqlalchemy.repositories.user_query import SqlAlchemyUserQuery
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal
from src.app.adapters.outbound.security.auth_context import JwtAuthContext
from src.app.adapters.outbound.security.jwt_service import JwtService
from src.app.adapters.outbound.security.password_hasher import PasswordHasher
from src.app.application.auth.ports import UserQueryPort
from src.app.application.auth.use_cases.login import LoginUseCase
from src.app.application.auth.use_cases.refresh_token import RefreshTokenUseCase
from src.app.application.idea.use_cases.add_progress_log import AddProgressLogUseCase
from src.app.application.idea.use_cases.create_idea import CreateIdeaUseCase
from src.app.application.idea.use_cases.delete_idea import DeleteIdeaUseCase
from src.app.application.idea.use_cases.get_idea_detail import GetIdeaDetailUseCase
from src.app.application.idea.use_cases.list_ideas import ListIdeasUseCase
from src.app.application.idea.use_cases.list_progress_logs import ListProgressLogsUseCase
from src.app.application.idea.use_cases.rating import GetIdeaRatingUseCase, RateIdeaUseCase, UpdateIdeaRatingUseCase
from src.app.application.idea.use_cases.update_idea import UpdateIdeaUseCase
from src.app.bootstrap.settings import settings

_repo = SqlAlchemyIdeaRepository(SessionLocal)
_progress_logs_repo = SqlAlchemyProgressLogRepository(SessionLocal)
_ratings_repo = SqlAlchemyRatingRepository(SessionLocal)
_password_hasher = PasswordHasher()
_users_query = cast(UserQueryPort, SqlAlchemyUserQuery(SessionLocal))
_token_service = JwtService(
    secret=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    expire_minutes=settings.JWT_EXPIRE_MINUTES,
    refresh_expire_minutes=settings.JWT_REFRESH_EXPIRE_MINUTES,
)

def get_create_idea_use_case_for_claims(claims: dict) -> CreateIdeaUseCase:
    return CreateIdeaUseCase(repository=_repo, auth_ctx=JwtAuthContext(claims))


def get_list_ideas_use_case_for_claims(claims: dict) -> ListIdeasUseCase:
    return ListIdeasUseCase(repository=_repo, auth_ctx=JwtAuthContext(claims))


def get_idea_detail_use_case_for_claims(claims: dict) -> GetIdeaDetailUseCase:
    return GetIdeaDetailUseCase(repository=_repo, auth_ctx=JwtAuthContext(claims))


def get_update_idea_use_case_for_claims(claims: dict) -> UpdateIdeaUseCase:
    return UpdateIdeaUseCase(repository=_repo, auth_ctx=JwtAuthContext(claims), log_repository=_progress_logs_repo)


def get_delete_idea_use_case_for_claims(claims: dict) -> DeleteIdeaUseCase:
    return DeleteIdeaUseCase(repository=_repo, auth_ctx=JwtAuthContext(claims))


def get_add_progress_log_use_case_for_claims(claims: dict) -> AddProgressLogUseCase:
    return AddProgressLogUseCase(
        idea_repository=_repo,
        log_repository=_progress_logs_repo,
        auth_ctx=JwtAuthContext(claims),
    )


def get_list_progress_logs_use_case_for_claims(claims: dict) -> ListProgressLogsUseCase:
    return ListProgressLogsUseCase(
        idea_repository=_repo,
        log_repository=_progress_logs_repo,
        auth_ctx=JwtAuthContext(claims),
    )


def get_rate_idea_use_case_for_claims(claims: dict) -> RateIdeaUseCase:
    return RateIdeaUseCase(
        idea_repository=_repo,
        rating_repository=_ratings_repo,
        auth_ctx=JwtAuthContext(claims),
    )


def get_update_idea_rating_use_case_for_claims(claims: dict) -> UpdateIdeaRatingUseCase:
    return UpdateIdeaRatingUseCase(
        idea_repository=_repo,
        rating_repository=_ratings_repo,
        auth_ctx=JwtAuthContext(claims),
    )


def get_idea_rating_use_case_for_claims(claims: dict) -> GetIdeaRatingUseCase:
    return GetIdeaRatingUseCase(
        idea_repository=_repo,
        rating_repository=_ratings_repo,
        auth_ctx=JwtAuthContext(claims),
    )


def get_token_service() -> JwtService:
    return _token_service


def get_login_use_case() -> LoginUseCase:
    return LoginUseCase(users=_users_query, hasher=_password_hasher, tokens=_token_service)


def get_refresh_token_use_case() -> RefreshTokenUseCase:
    return RefreshTokenUseCase(tokens=_token_service)
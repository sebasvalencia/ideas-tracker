from src.app.application.idea.dto import RateIdeaInput, RatingOutput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRepositoryPort, RatingRecord, RatingRepositoryPort


def _to_output(row: RatingRecord) -> RatingOutput:
    return RatingOutput(
        id=row.id,
        idea_id=row.idea_id,
        rating=row.rating,
        summary=row.summary,
        created_at=row.created_at,
    )


def _validate_access_and_state(
    *,
    idea_id: int,
    idea_repository: IdeaRepositoryPort,
    auth_ctx: AuthContextPort,
) -> None:
    idea = idea_repository.get_active_by_id(idea_id=idea_id)
    if idea is None:
        raise NotFoundError("idea not found")

    user = auth_ctx.current_user()
    if idea.owner_id != user.user_id and user.role != "admin":
        raise ForbiddenError("forbidden")

    if idea.status != "completed":
        raise DomainValidationError("rating allowed only for finished ideas")


def _validate_rating_value(value: int) -> None:
    if not 1 <= value <= 10:
        raise DomainValidationError("rating must be between 1 and 10")


class RateIdeaUseCase:
    def __init__(
        self,
        *,
        idea_repository: IdeaRepositoryPort,
        rating_repository: RatingRepositoryPort,
        auth_ctx: AuthContextPort,
    ) -> None:
        self._idea_repository = idea_repository
        self._rating_repository = rating_repository
        self._auth_ctx = auth_ctx

    def execute(self, *, idea_id: int, data: RateIdeaInput) -> RatingOutput:
        _validate_access_and_state(idea_id=idea_id, idea_repository=self._idea_repository, auth_ctx=self._auth_ctx)
        _validate_rating_value(data.rating)

        existing = self._rating_repository.get_by_idea(idea_id=idea_id)
        if existing is not None:
            raise DomainValidationError("rating already exists")

        created = self._rating_repository.create(
            idea_id=idea_id,
            rating=data.rating,
            summary=data.summary,
        )
        return _to_output(created)


class UpdateIdeaRatingUseCase:
    def __init__(
        self,
        *,
        idea_repository: IdeaRepositoryPort,
        rating_repository: RatingRepositoryPort,
        auth_ctx: AuthContextPort,
    ) -> None:
        self._idea_repository = idea_repository
        self._rating_repository = rating_repository
        self._auth_ctx = auth_ctx

    def execute(self, *, idea_id: int, data: RateIdeaInput) -> RatingOutput:
        _validate_access_and_state(idea_id=idea_id, idea_repository=self._idea_repository, auth_ctx=self._auth_ctx)
        _validate_rating_value(data.rating)

        existing = self._rating_repository.get_by_idea(idea_id=idea_id)
        if existing is None:
            raise NotFoundError("rating not found")

        updated = self._rating_repository.update(
            idea_id=idea_id,
            rating=data.rating,
            summary=data.summary,
        )
        return _to_output(updated)


class GetIdeaRatingUseCase:
    def __init__(
        self,
        *,
        idea_repository: IdeaRepositoryPort,
        rating_repository: RatingRepositoryPort,
        auth_ctx: AuthContextPort,
    ) -> None:
        self._idea_repository = idea_repository
        self._rating_repository = rating_repository
        self._auth_ctx = auth_ctx

    def execute(self, *, idea_id: int) -> RatingOutput:
        _validate_access_and_state(idea_id=idea_id, idea_repository=self._idea_repository, auth_ctx=self._auth_ctx)

        row = self._rating_repository.get_by_idea(idea_id=idea_id)
        if row is None:
            raise NotFoundError("rating not found")
        return _to_output(row)

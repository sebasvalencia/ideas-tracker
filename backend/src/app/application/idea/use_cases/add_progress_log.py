from src.app.application.idea.dto import AddProgressLogInput, ProgressLogOutput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRepositoryPort, ProgressLogRecord, ProgressLogRepositoryPort


class AddProgressLogUseCase:
    def __init__(
        self,
        *,
        idea_repository: IdeaRepositoryPort,
        log_repository: ProgressLogRepositoryPort,
        auth_ctx: AuthContextPort,
    ) -> None:
        self._idea_repository = idea_repository
        self._log_repository = log_repository
        self._auth_ctx = auth_ctx

    def execute(self, *, idea_id: int, data: AddProgressLogInput) -> ProgressLogOutput:
        comment = data.comment.strip()
        if not comment:
            raise DomainValidationError("comment must not be empty")

        idea = self._idea_repository.get_active_by_id(idea_id=idea_id)
        if idea is None:
            raise NotFoundError("idea not found")

        user = self._auth_ctx.current_user()
        if idea.owner_id != user.user_id and user.role != "admin":
            raise ForbiddenError("forbidden")

        created = self._log_repository.create(
            idea_id=idea.id,
            author_id=user.user_id,
            comment=comment,
            progress_snapshot=idea.execution_percentage,
            status_snapshot=idea.status,
        )
        return self._to_output(created)

    @staticmethod
    def _to_output(record: ProgressLogRecord) -> ProgressLogOutput:
        return ProgressLogOutput(
            id=record.id,
            idea_id=record.idea_id,
            author_id=record.author_id,
            comment=record.comment,
            progress_snapshot=record.progress_snapshot,
            status_snapshot=record.status_snapshot,
            created_at=record.created_at,
        )

from src.app.application.idea.dto import ProgressLogOutput
from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRepositoryPort, ProgressLogRepositoryPort


class ListProgressLogsUseCase:
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

    def execute(self, *, idea_id: int) -> list[ProgressLogOutput]:
        idea = self._idea_repository.get_active_by_id(idea_id=idea_id)
        if idea is None:
            raise NotFoundError("idea not found")

        user = self._auth_ctx.current_user()
        if idea.owner_id != user.user_id and user.role != "admin":
            raise ForbiddenError("forbidden")

        rows = self._log_repository.list_by_idea(idea_id=idea_id)
        return [
            ProgressLogOutput(
                id=row.id,
                idea_id=row.idea_id,
                author_id=row.author_id,
                comment=row.comment,
                progress_snapshot=row.progress_snapshot,
                status_snapshot=row.status_snapshot,
                created_at=row.created_at,
            )
            for row in rows
        ]

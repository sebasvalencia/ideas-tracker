from datetime import datetime

from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRepositoryPort


class DeleteIdeaUseCase:
    def __init__(self, repository: IdeaRepositoryPort, auth_ctx: AuthContextPort) -> None:
        self._repository = repository
        self._auth_ctx = auth_ctx

    def execute(self, *, idea_id: int) -> None:
        idea = self._repository.get_active_by_id(idea_id=idea_id)
        if idea is None:
            raise NotFoundError("idea not found")

        user = self._auth_ctx.current_user()
        if idea.owner_id != user.user_id and user.role != "admin":
            raise ForbiddenError("forbidden")

        self._repository.soft_delete(idea_id=idea_id, deleted_at=datetime.now())

from src.app.application.idea.dto import CreateIdeaOutput
from src.app.application.idea.errors import ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRecord, IdeaRepositoryPort


class GetIdeaDetailUseCase:
    def __init__(self, repository: IdeaRepositoryPort, auth_ctx: AuthContextPort) -> None:
        self._repository = repository
        self._auth_ctx = auth_ctx

    def execute(self, idea_id: int) -> CreateIdeaOutput:
        idea = self._repository.get_active_by_id(idea_id=idea_id)
        if idea is None:
            raise NotFoundError("idea not found")

        user = self._auth_ctx.current_user()
        if idea.owner_id != user.user_id and user.role != "admin":
            raise ForbiddenError("forbidden")

        return self._to_output(idea)

    @staticmethod
    def _to_output(idea: IdeaRecord) -> CreateIdeaOutput:
        return CreateIdeaOutput(
            id=idea.id,
            owner_id=idea.owner_id,
            title=idea.title,
            description=idea.description,
            status=idea.status,
            execution_percentage=idea.execution_percentage,
            created_at=idea.created_at,
            updated_at=idea.updated_at,
            deleted_at=idea.deleted_at,
        )

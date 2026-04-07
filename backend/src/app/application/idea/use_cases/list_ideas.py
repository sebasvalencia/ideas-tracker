from src.app.application.idea.dto import CreateIdeaOutput, ListIdeasInput
from src.app.application.idea.ports import AuthContextPort, IdeaRecord, IdeaRepositoryPort


class ListIdeasUseCase:
    def __init__(self, repository: IdeaRepositoryPort, auth_ctx: AuthContextPort) -> None:
        self._repository = repository
        self._auth_ctx = auth_ctx

    def execute(self, data: ListIdeasInput) -> list[CreateIdeaOutput]:
        user = self._auth_ctx.current_user()
        ideas = self._repository.list_active(
            owner_id=user.user_id,
            status=data.status,
            limit=data.limit,
            offset=data.offset,
        )
        return [self._to_output(idea) for idea in ideas]

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

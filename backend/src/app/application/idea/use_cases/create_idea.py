from src.app.application.idea.dto import CreateIdeaInput, CreateIdeaOutput
from src.app.application.idea.errors import DomainValidationError
from src.app.application.idea.ports import AuthContextPort, IdeaRepositoryPort

class CreateIdeaUseCase:
    def __init__(self, repository: IdeaRepositoryPort, auth_ctx: AuthContextPort) -> None:
        self._repository = repository
        self._auth_ctx = auth_ctx
    
    def execute(self, data: CreateIdeaInput) -> CreateIdeaOutput:
        if not data.title.strip():
            raise DomainValidationError("title must not be empty")
        if not data.description.strip():
            raise DomainValidationError("description must not be empty")
        
        user = self._auth_ctx.current_user()
        created = self._repository.create(
            owner_id=user.user_id,
            title=data.title.strip(),
            description=data.description.strip(),
        )
        return CreateIdeaOutput(
            id=created.id,
            owner_id=created.owner_id,
            title=created.title,
            description=created.description,
            status=created.status,
            execution_percentage=created.execution_percentage,
            created_at=created.created_at,
            updated_at=created.updated_at,
            deleted_at=created.deleted_at,
        )

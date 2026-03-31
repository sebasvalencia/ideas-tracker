from src.app.adapters.outbound.persistence.in_memory.idea_repository import InMemoryIdeaRepository
from src.app.adapters.outbound.security.auth_context import StaticAuthContext
from src.app.application.idea.use_cases.create_idea import CreateIdeaUseCase

_repo = InMemoryIdeaRepository()
_auth = StaticAuthContext()

def get_create_idea_use_case() -> CreateIdeaUseCase:
    return CreateIdeaUseCase(repository=_repo, auth_ctx=_auth)
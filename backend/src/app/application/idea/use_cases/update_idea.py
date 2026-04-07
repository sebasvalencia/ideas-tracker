from datetime import datetime

from src.app.application.idea.dto import CreateIdeaOutput, UpdateIdeaInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.application.idea.ports import AuthContextPort, IdeaRecord, IdeaRepositoryPort, ProgressLogRepositoryPort
from src.app.application.idea.services.progress_log_policy import system_log_message, should_create_system_log

ALLOWED_STATUSES = {"idea", "in_progress", "completed"}


class UpdateIdeaUseCase:
    def __init__(
        self,
        repository: IdeaRepositoryPort,
        auth_ctx: AuthContextPort,
        log_repository: ProgressLogRepositoryPort | None = None,
    ) -> None:
        self._repository = repository
        self._auth_ctx = auth_ctx
        self._log_repository = log_repository

    def execute(self, *, idea_id: int, patch: UpdateIdeaInput) -> CreateIdeaOutput:
        current = self._repository.get_active_by_id(idea_id=idea_id)
        if current is None:
            raise NotFoundError("idea not found")

        user = self._auth_ctx.current_user()
        if current.owner_id != user.user_id and user.role != "admin":
            raise ForbiddenError("forbidden")

        next_status = self._normalize_status(patch.status) if patch.status is not None else current.status
        next_progress = patch.execution_percentage if patch.execution_percentage is not None else current.execution_percentage
        next_title = patch.title.strip() if patch.title is not None else current.title
        next_description = patch.description.strip() if patch.description is not None else current.description

        if not next_title:
            raise DomainValidationError("title must not be empty")
        if not next_description:
            raise DomainValidationError("description must not be empty")
        if not 0 <= next_progress <= 100:
            raise DomainValidationError("execution_percentage must be between 0 and 100")
        if next_status == "completed" and next_progress != 100:
            raise DomainValidationError("completed requires execution_percentage=100")

        updated = self._repository.update(
            idea=IdeaRecord(
                id=current.id,
                owner_id=current.owner_id,
                title=next_title,
                description=next_description,
                status=next_status,
                execution_percentage=next_progress,
                created_at=current.created_at,
                updated_at=datetime.now(),
                deleted_at=current.deleted_at,
            )
        )

        if self._log_repository is not None and should_create_system_log(
            current.status,
            current.execution_percentage,
            updated.status,
            updated.execution_percentage,
        ):
            self._log_repository.create(
                idea_id=updated.id,
                author_id=user.user_id,
                comment=system_log_message(
                    current.status,
                    current.execution_percentage,
                    updated.status,
                    updated.execution_percentage,
                ),
                progress_snapshot=updated.execution_percentage,
                status_snapshot=updated.status,
            )
        return self._to_output(updated)

    @staticmethod
    def _normalize_status(status: str) -> str:
        normalized = status.strip().lower()
        if normalized == "terminada":
            normalized = "completed"
        if normalized not in ALLOWED_STATUSES:
            raise DomainValidationError("invalid status")
        return normalized

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

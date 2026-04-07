from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.dto import AddProgressLogInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.bootstrap.container import get_add_progress_log_use_case_for_claims, get_list_progress_logs_use_case_for_claims

router = APIRouter(prefix="/api/v1/ideas", tags=["logs"])


class AddProgressLogRequest(BaseModel):
    comment: str


@router.post("/{idea_id}/logs", status_code=201)
def add_progress_log(idea_id: int, payload: AddProgressLogRequest, user: dict = Depends(get_current_user)):
    use_case = get_add_progress_log_use_case_for_claims(user)
    try:
        result = use_case.execute(
            idea_id=idea_id,
            data=AddProgressLogInput(comment=payload.comment),
        )
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc


@router.get("/{idea_id}/logs", status_code=200)
def list_progress_logs(idea_id: int, user: dict = Depends(get_current_user)):
    use_case = get_list_progress_logs_use_case_for_claims(user)
    try:
        result = use_case.execute(idea_id=idea_id)
        return [item.__dict__ for item in result]
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc

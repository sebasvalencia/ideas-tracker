from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.dto import CreateIdeaInput, ListIdeasInput, UpdateIdeaInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.bootstrap.container import (
    get_create_idea_use_case_for_claims,
    get_delete_idea_use_case_for_claims,
    get_idea_detail_use_case_for_claims,
    get_list_ideas_use_case_for_claims,
    get_update_idea_use_case_for_claims,
)

router = APIRouter(prefix="/api/v1/ideas", tags=["ideas"])

class CreateIdeaRequest(BaseModel):
    title: str
    description: str


class UpdateIdeaRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    execution_percentage: float | None = None


@router.post("", status_code=201)
def create_idea(payload: CreateIdeaRequest, user: dict = Depends(get_current_user)):
    use_case = get_create_idea_use_case_for_claims(user)
    try:
        result = use_case.execute(CreateIdeaInput(title=payload.title, description=payload.description))
        return result.__dict__
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc


@router.get("", status_code=200)
def list_ideas(
    user: dict = Depends(get_current_user),
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    use_case = get_list_ideas_use_case_for_claims(user)
    result = use_case.execute(ListIdeasInput(status=status_filter, limit=limit, offset=offset))
    return [item.__dict__ for item in result]


@router.get("/{idea_id}", status_code=200)
def get_idea_detail(idea_id: int, user: dict = Depends(get_current_user)):
    use_case = get_idea_detail_use_case_for_claims(user)
    try:
        result = use_case.execute(idea_id=idea_id)
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.patch("/{idea_id}", status_code=200)
def update_idea(idea_id: int, payload: UpdateIdeaRequest, user: dict = Depends(get_current_user)):
    use_case = get_update_idea_use_case_for_claims(user)
    try:
        result = use_case.execute(
            idea_id=idea_id,
            patch=UpdateIdeaInput(
                title=payload.title,
                description=payload.description,
                status=payload.status,
                execution_percentage=payload.execution_percentage,
            ),
        )
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc


@router.delete("/{idea_id}", status_code=204)
def delete_idea(idea_id: int, user: dict = Depends(get_current_user)):
    use_case = get_delete_idea_use_case_for_claims(user)
    try:
        use_case.execute(idea_id=idea_id)
        return None
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
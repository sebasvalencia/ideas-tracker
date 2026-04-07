from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.app.adapters.inbound.rest.auth_dependencies import get_current_user
from src.app.application.idea.dto import RateIdeaInput
from src.app.application.idea.errors import DomainValidationError, ForbiddenError, NotFoundError
from src.app.bootstrap.container import (
    get_idea_rating_use_case_for_claims,
    get_rate_idea_use_case_for_claims,
    get_update_idea_rating_use_case_for_claims,
)

router = APIRouter(prefix="/api/v1/ideas", tags=["ratings"])


class RateIdeaRequest(BaseModel):
    rating: int
    summary: str | None = None


@router.post("/{idea_id}/rating", status_code=201)
def rate_idea(idea_id: int, payload: RateIdeaRequest, user: dict = Depends(get_current_user)):
    use_case = get_rate_idea_use_case_for_claims(user)
    try:
        result = use_case.execute(
            idea_id=idea_id,
            data=RateIdeaInput(rating=payload.rating, summary=payload.summary),
        )
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc


@router.patch("/{idea_id}/rating", status_code=200)
def update_idea_rating(idea_id: int, payload: RateIdeaRequest, user: dict = Depends(get_current_user)):
    use_case = get_update_idea_rating_use_case_for_claims(user)
    try:
        result = use_case.execute(
            idea_id=idea_id,
            data=RateIdeaInput(rating=payload.rating, summary=payload.summary),
        )
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc


@router.get("/{idea_id}/rating", status_code=200)
def get_idea_rating(idea_id: int, user: dict = Depends(get_current_user)):
    use_case = get_idea_rating_use_case_for_claims(user)
    try:
        result = use_case.execute(idea_id=idea_id)
        return result.__dict__
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ForbiddenError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except DomainValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc

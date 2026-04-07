from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.app.application.idea.dto import CreateIdeaInput
from src.app.bootstrap.container import get_create_idea_use_case

router = APIRouter(prefix="/api/v1/ideas", tags=["ideas"])

class CreateIdeaRequest(BaseModel):
    title: str
    description: str

@router.post("", status_code=201)
def create_idea(payload: CreateIdeaRequest):
    use_case = get_create_idea_use_case()
    try:
        result = use_case.execute(CreateIdeaInput(title=payload.title, description=payload.description))
        return result.__dict__
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
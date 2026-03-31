from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CreateIdeaInput:
    title: str
    description: str

@dataclass(frozen=True)
class CreateIdeaOutput:
    id: int
    owner_id: int
    title: str
    description: str
    status: str
    execution_percentage: float
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
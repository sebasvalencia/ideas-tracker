from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CreateIdeaInput:
    title: str
    description: str


@dataclass(frozen=True)
class ListIdeasInput:
    status: str | None = None
    limit: int = 20
    offset: int = 0


@dataclass(frozen=True)
class UpdateIdeaInput:
    title: str | None = None
    description: str | None = None
    status: str | None = None
    execution_percentage: float | None = None


@dataclass(frozen=True)
class AddProgressLogInput:
    comment: str


@dataclass(frozen=True)
class RateIdeaInput:
    rating: int
    summary: str | None = None


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


@dataclass(frozen=True)
class ProgressLogOutput:
    id: int
    idea_id: int
    author_id: int
    comment: str
    progress_snapshot: float
    status_snapshot: str
    created_at: datetime


@dataclass(frozen=True)
class RatingOutput:
    id: int
    idea_id: int
    rating: int
    summary: str | None
    created_at: datetime
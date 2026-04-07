from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

@dataclass(frozen=True)
class AuthUser:
    user_id: int
    email: str
    role: str

@dataclass(frozen=True)
class IdeaRecord:
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
class ProgressLogRecord:
    id: int
    idea_id: int
    author_id: int
    comment: str
    progress_snapshot: float
    status_snapshot: str
    created_at: datetime

@dataclass(frozen=True)
class RatingRecord:
    id: int
    idea_id: int
    rating: int
    summary: str | None
    created_at: datetime

class IdeaRepositoryPort(Protocol):
    def create(self, *, owner_id: int, title:str, description:str) -> IdeaRecord: ...
    def list_active(self, *, owner_id: int, status: str | None, limit: int, offset: int) -> list[IdeaRecord]: ...
    def get_active_by_id(self, *, idea_id: int) -> IdeaRecord | None: ...
    def update(self, *, idea: IdeaRecord) -> IdeaRecord: ...
    def soft_delete(self, *, idea_id: int, deleted_at: datetime) -> None: ...

class ProgressLogRepositoryPort(Protocol):
    def create(self, *, idea_id: int, author_id: int, comment: str, progress_snapshot: float, status_snapshot: str) -> ProgressLogRecord: ...
    def list_by_idea(self, *, idea_id: int) -> list[ProgressLogRecord]: ...

class RatingRepositoryPort(Protocol):
    def get_by_idea(self, *, idea_id: int) -> RatingRecord | None: ...
    def create(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord: ...
    def update(self, *, idea_id: int, rating: int, summary: str | None) -> RatingRecord: ...

class AuthContextPort(Protocol):
    def current_user(self) -> AuthUser:
        ...
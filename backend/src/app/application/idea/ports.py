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

class IdeaRepositoryPort(Protocol):
    def create(self, *, owner_id: int, title:str, description:str) -> "IdeaRecord":
        ...
    
class AuthContextPort(Protocol):
    def current_user(self) -> AuthUser:
        ...
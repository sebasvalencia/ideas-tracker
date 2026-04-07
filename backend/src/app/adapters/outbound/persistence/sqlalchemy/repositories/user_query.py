from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.app.adapters.outbound.persistence.sqlalchemy.models_auth import User


@dataclass(frozen=True)
class SqlAlchemyUserRecord:
    id: int
    email: str
    password_hash: str
    roles: list[str]
    is_active: bool


class SqlAlchemyUserQuery:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def get_by_email(self, email: str) -> SqlAlchemyUserRecord | None:
        with self._session_factory() as db:
            user = db.scalar(select(User).where(User.email == email))
            if not user:
                return None
            roles = [role.name for role in user.roles]
            return SqlAlchemyUserRecord(
                id=user.id,
                email=user.email,
                password_hash=user.password_hash,
                roles=roles,
                is_active=user.is_active,
            )

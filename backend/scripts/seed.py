import sys
from pathlib import Path
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import select, update as sa_update

# Allow running as: `python scripts/seed.py`
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app.adapters.outbound.persistence.sqlalchemy.models_auth import Role, User
from src.app.adapters.outbound.persistence.sqlalchemy.models_idea import Idea, IdeaStatus
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal

# Use Argon2 as default password hashing algorithm.
pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def main() -> None:
    with SessionLocal() as db:
        desired_statuses = (
            {"code": "idea", "name": "Idea", "is_terminal": False, "sort_order": 10},
            {"code": "in_progress", "name": "In Progress", "is_terminal": False, "sort_order": 20},
            {"code": "completed", "name": "Completed", "is_terminal": True, "sort_order": 30},
        )

        # Upsert current catalog statuses to keep names/order consistent.
        for status in desired_statuses:
            status_exists = db.scalar(select(IdeaStatus).where(IdeaStatus.code == status["code"]))
            if not status_exists:
                db.add(IdeaStatus(**status))
            else:
                status_exists.name = status["name"]
                status_exists.is_terminal = status["is_terminal"]
                status_exists.sort_order = status["sort_order"]

        db.flush()

        # Backward compatibility cleanup:
        # If old "terminada" exists, migrate references to "completed" and remove it.
        old_done = db.scalar(select(IdeaStatus).where(IdeaStatus.code == "terminada"))
        completed = db.scalar(select(IdeaStatus).where(IdeaStatus.code == "completed"))
        if old_done:
            if completed and old_done.id != completed.id:
                db.execute(
                    sa_update(Idea)
                    .where(Idea.status_id == old_done.id)
                    .values(status_id=completed.id, updated_at=datetime.utcnow())
                )
                db.delete(old_done)
            else:
                old_done.code = "completed"
                old_done.name = "Completed"
                old_done.is_terminal = True
                old_done.sort_order = 30

        for role_name in ("admin", "user"):
            role_exists = db.scalar(select(Role).where(Role.name == role_name))
            if not role_exists:
                db.add(Role(name=role_name))
        db.flush()

        admin_email = "admin@ideas.local"
        admin = db.scalar(select(User).where(User.email == admin_email))
        if not admin:
            db.add(
                User(
                    email=admin_email,
                    password_hash=pwd.hash("ChangeMe123!"),
                    is_active=True,
                )
            )
        db.commit()


if __name__ == "__main__":
    main()
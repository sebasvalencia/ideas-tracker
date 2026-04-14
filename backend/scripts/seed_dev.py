"""
seed_dev.py — Demo fixtures for development and CI only.

Creates the admin user (admin@ideas.com / ChangeMe123!) used in E2E and BDD
tests. Catalog data (statuses, roles) is handled by Alembic migrations and
does NOT need to be here.

Refuses to run when APP_ENV=production.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.app.bootstrap.settings import settings  # noqa: E402


def main() -> None:
    if settings.APP_ENV == "production":
        print(
            "ERROR: seed_dev.py refused to run in production. "
            "Use proper user-management tooling instead.",
            file=sys.stderr,
        )
        sys.exit(1)

    from passlib.context import CryptContext  # noqa: PLC0415
    from sqlalchemy import select  # noqa: PLC0415

    from src.app.adapters.outbound.persistence.sqlalchemy.models_auth import Role, User  # noqa: PLC0415
    from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal  # noqa: PLC0415

    pwd = CryptContext(schemes=["argon2"], deprecated="auto")

    with SessionLocal() as db:
        admin_email = "admin@ideas.com"
        existing = db.scalar(select(User).where(User.email == admin_email))
        if existing:
            print(f"seed_dev: {admin_email} already exists, skipping.")
            return

        admin_role = db.scalar(select(Role).where(Role.name == "admin"))
        admin = User(
            email=admin_email,
            password_hash=pwd.hash("ChangeMe123!"),
            is_active=True,
        )
        if admin_role:
            admin.roles = [admin_role]
        db.add(admin)
        db.commit()
        print(f"seed_dev: created {admin_email}.")


if __name__ == "__main__":
    main()

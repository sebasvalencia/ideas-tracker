"""
manage_user.py — User management CLI for all environments including production.

Commands
--------
create-admin    Create (or promote) a user with the admin role.
reset-password  Reset the password for an existing user.

Usage (on the server via SSH)
------------------------------
    uv run python scripts/manage_user.py create-admin \\
        --email admin@mycompany.com --password 'SuperSecure123!'

    uv run python scripts/manage_user.py reset-password \\
        --email admin@mycompany.com --password 'NewPassword456!'

The script reads DATABASE_URL (and other settings) from the environment or
from a .env file in the backend directory, same as the app itself.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MIN_PASSWORD_LENGTH = 10


def _validate_password(password: str) -> None:
    if len(password) < MIN_PASSWORD_LENGTH:
        print(f"ERROR: password must be at least {MIN_PASSWORD_LENGTH} characters.", file=sys.stderr)
        sys.exit(1)
    if password.isalpha() or password.isdigit():
        print("ERROR: password must mix letters and numbers/symbols.", file=sys.stderr)
        sys.exit(1)


def cmd_create_admin(email: str, password: str) -> None:
    _validate_password(password)

    from passlib.context import CryptContext  # noqa: PLC0415
    from sqlalchemy import select  # noqa: PLC0415

    from src.app.adapters.outbound.persistence.sqlalchemy.models_auth import Role, User  # noqa: PLC0415
    from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal  # noqa: PLC0415

    pwd = CryptContext(schemes=["argon2"], deprecated="auto")

    with SessionLocal() as db:
        admin_role = db.scalar(select(Role).where(Role.name == "admin"))
        if not admin_role:
            print("ERROR: 'admin' role not found. Run 'alembic upgrade head' first.", file=sys.stderr)
            sys.exit(1)

        user = db.scalar(select(User).where(User.email == email))
        if user:
            user.password_hash = pwd.hash(password)
            user.is_active = True
            if admin_role not in user.roles:
                user.roles.append(admin_role)
            db.commit()
            print(f"OK: updated existing user '{email}' with admin role and new password.")
        else:
            new_user = User(
                email=email,
                password_hash=pwd.hash(password),
                is_active=True,
                roles=[admin_role],
            )
            db.add(new_user)
            db.commit()
            print(f"OK: created admin user '{email}'.")


def cmd_reset_password(email: str, password: str) -> None:
    _validate_password(password)

    from passlib.context import CryptContext  # noqa: PLC0415
    from sqlalchemy import select  # noqa: PLC0415

    from src.app.adapters.outbound.persistence.sqlalchemy.models_auth import User  # noqa: PLC0415
    from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal  # noqa: PLC0415

    pwd = CryptContext(schemes=["argon2"], deprecated="auto")

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        if not user:
            print(f"ERROR: user '{email}' not found.", file=sys.stderr)
            sys.exit(1)
        user.password_hash = pwd.hash(password)
        db.commit()
        print(f"OK: password updated for '{email}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ideas Tracker user management")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create-admin", help="Create or promote a user to admin")
    p_create.add_argument("--email", required=True)
    p_create.add_argument("--password", required=True)

    p_reset = sub.add_parser("reset-password", help="Reset a user's password")
    p_reset.add_argument("--email", required=True)
    p_reset.add_argument("--password", required=True)

    args = parser.parse_args()

    if args.command == "create-admin":
        cmd_create_admin(args.email, args.password)
    elif args.command == "reset-password":
        cmd_reset_password(args.email, args.password)


if __name__ == "__main__":
    main()

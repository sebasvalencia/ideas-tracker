"""
seed.py — DEPRECATED.

Catalog data (statuses, roles) is now handled by the Alembic migration
`a2b3c4d5e6f7_seed_catalog`. Demo user creation was moved to seed_dev.py.

This file is kept for backward compatibility and simply delegates to seed_dev.
"""
import warnings

warnings.warn(
    "scripts/seed.py is deprecated. Use 'alembic upgrade head' for catalog data "
    "and 'scripts/seed_dev.py' for the demo admin user.",
    DeprecationWarning,
    stacklevel=1,
)

from seed_dev import main  # noqa: E402

if __name__ == "__main__":
    main()

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from scripts.seed_dev import main as seed_main
from src.app.adapters.outbound.persistence.sqlalchemy.session import SessionLocal
from src.main import app


@pytest.fixture(scope="session")
def bdd_client() -> Generator[TestClient, None, None]:
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Postgres not available for BDD tests: {exc}")

    seed_main()
    with TestClient(app) as client:
        yield client


@pytest.fixture
def bdd_context() -> dict:
    return {}

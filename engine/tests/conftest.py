"""Shared fixtures. DB-backed tests skip automatically when Postgres is unreachable."""

from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from kge.db import engine


def _db_available() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        return True
    except Exception:
        return False


@pytest.fixture
def db_session():
    """Session wrapped in a transaction that is rolled back after each test."""
    if not _db_available():
        pytest.skip("Postgres not available (bring it up with `docker compose up -d db`)")
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()

"""Shared fixtures.

DB-backed tests run against a dedicated ``kosmographica_test`` database (created on the
fly) so they never see — or disturb — seeded dev data. Each test runs in a transaction
that is rolled back on teardown. Everything skips automatically if Postgres is unreachable.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from kge.config import settings
from kge.models import Base

_TEST_DB = "kosmographica_test"
_TEST_URL = settings.database_url.rsplit("/", 1)[0] + f"/{_TEST_DB}"


def _server_reachable() -> bool:
    try:
        eng = create_engine(settings.database_url)
        with eng.connect() as conn:
            conn.execute(text("select 1"))
        eng.dispose()
        return True
    except Exception:
        return False


def _ensure_test_db() -> None:
    admin = create_engine(settings.database_url, isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.execute(
            text("select 1 from pg_database where datname = :n"), {"n": _TEST_DB}
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{_TEST_DB}"'))
    admin.dispose()


@pytest.fixture(scope="session")
def _test_engine():
    if not _server_reachable():
        pytest.skip("Postgres not available (bring it up with `docker compose up -d db`)")
    _ensure_test_db()
    engine = create_engine(_TEST_URL, future=True)
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_entities_fts ON entities USING GIN "
                "(to_tsvector('simple', coalesce(label,'') || ' ' || coalesce(data->>'description','')))"
            )
        )
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(_test_engine):
    connection = _test_engine.connect()
    trans = connection.begin()
    SessionFactory = sessionmaker(bind=connection, expire_on_commit=False, future=True)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()

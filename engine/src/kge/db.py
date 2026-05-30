"""SQLAlchemy engine and session factory."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Transactional session scope; commits on success, rolls back on error."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

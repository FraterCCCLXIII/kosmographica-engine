"""SQLAlchemy engine and session factory."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

# Read endpoints fan out under concurrency (e.g. a browse page that prefetches many
# detail routes), so the pool is sized well above SQLAlchemy's default 5+10. A short
# pool_timeout makes an over-saturated server fail fast instead of blocking 30s.
engine = create_engine(
    settings.database_url,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
    pool_timeout=10,
)
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

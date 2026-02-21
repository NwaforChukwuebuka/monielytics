"""Database engine, session factory, and dependency."""
import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import DATABASE_URL
from app.models import Base

logger = logging.getLogger(__name__)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: yield a DB session and close it after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Context manager for scripts that need a session."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Create tables and indexes if they do not exist."""
    logger.info("Creating tables if not exist")
    # Composite indexes for analytics queries
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        for ddl in [
            "CREATE INDEX IF NOT EXISTS ix_activities_status_product ON activities (status, product)",
            "CREATE INDEX IF NOT EXISTS ix_activities_status_ts ON activities (status, event_timestamp)",
            "CREATE INDEX IF NOT EXISTS ix_activities_product_status ON activities (product, status)",
        ]:
            conn.execute(text(ddl))
            conn.commit()
    logger.info("Database schema initialized")

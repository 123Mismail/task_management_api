from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session, SQLModel
from .config import settings
from typing import Generator


# Configure engine with optimal settings for Neon PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # connections maintained in pool
    max_overflow=30,  # additional overflow connections
    pool_pre_ping=True,  # verify connections before use
    pool_recycle=3600,  # recycle connections after 1 hour
    pool_timeout=30,  # wait time for connections
    poolclass=QueuePool,
    echo=False  # set to True for debugging SQL queries
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session as a dependency for FastAPI"""
    with Session(engine) as session:
        yield session
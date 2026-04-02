import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import structlog

logger = structlog.get_logger()

# CNC_DB_PATH lets Tauri (or any caller) redirect the SQLite file to the
# OS-appropriate app-data directory.  Falls back to ./cnccalc.db for dev.
_db_path = os.environ.get("CNC_DB_PATH", "./cnccalc.db")
_db_url = f"sqlite+aiosqlite:///{_db_path}"

# Create async engine
engine = create_async_engine(
    _db_url,
    echo=False,
    connect_args={"check_same_thread": False},
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get database session
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()

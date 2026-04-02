"""
Entry point for PyInstaller bundling and Tauri sidecar use.

Responsibilities before starting uvicorn:
  1. Ensure the DB file's parent directory exists.
  2. Run SQLAlchemy create_all (idempotent schema migration).
  3. Run seed_data (idempotent — skips existing rows).
  4. Start uvicorn on 127.0.0.1:8000.

Environment variables:
  CNC_DB_PATH  — absolute path to the SQLite file.
                 Set by Tauri to <app-data-dir>/cnccalc.db.
                 Falls back to ./cnccalc.db for plain dev use.
"""
import asyncio
import os
import sys
from pathlib import Path

# Ensure the backend directory is on sys.path before any local imports.
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Guarantee the DB directory exists before SQLAlchemy tries to open the file.
db_path = os.environ.get("CNC_DB_PATH", str(backend_dir / "cnccalc.db"))
Path(db_path).parent.mkdir(parents=True, exist_ok=True)
# Normalise the env var so database.py and seed_data.py pick up the same value.
os.environ["CNC_DB_PATH"] = db_path


async def _init_db() -> None:
    """Create schema and seed reference data (both are idempotent)."""
    # Import here so the env var is already set when the module is loaded.
    from app.core.database import engine, Base
    from scripts.seed_data import seed_data

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await seed_data()


if __name__ == "__main__":
    asyncio.run(_init_db())

    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_config=None,
    )

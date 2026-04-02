# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the CNC Calc FastAPI sidecar.

Build:
    cd backend
    pyinstaller run_server.spec --distpath dist --workpath build/pyinstaller

Output: backend/dist/run_server  (macOS/Linux)
        backend/dist/run_server.exe  (Windows)
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# ---------------------------------------------------------------------------
# Hidden imports — packages PyInstaller cannot discover via static analysis
# ---------------------------------------------------------------------------

hidden_imports = (
    # Local packages
    collect_submodules("engine")
    + collect_submodules("app")
    + collect_submodules("models")
    + collect_submodules("services")
    + collect_submodules("schemas")
    + collect_submodules("scripts")
    # uvicorn internals (not reachable via import graph)
    + [
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.loops.asyncio",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.http.h11_impl",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
    ]
    # DB / async
    + ["aiosqlite", "sqlalchemy.dialects.sqlite", "greenlet"]
    # Pydantic
    + ["pydantic_settings", "pydantic.deprecated.class_validators"]
    # Logging
    + ["structlog"]
)

# ---------------------------------------------------------------------------
# Data files — non-Python assets that must travel with the binary
# ---------------------------------------------------------------------------

datas = [
    # Alembic migration scripts (needed if you switch to alembic upgrade head)
    ("alembic", "alembic"),
    ("alembic.ini", "."),
]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

a = Analysis(
    ["run_server.py"],
    pathex=["."],          # backend/ is on sys.path
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Strip packages we removed during the Tauri refactor
    excludes=["psycopg2", "asyncpg", "redis", "boto3", "botocore",
              "tkinter", "matplotlib", "numpy"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="run_server",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # Keep console=True so logs are visible during development / troubleshooting.
    # Change to False for a polished production release on Windows.
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

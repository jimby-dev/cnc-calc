# Phase 8 — Python Sidecar Packaging

## Goal
Bundle the FastAPI backend as a self-contained executable so Tauri can spawn and kill it automatically. The end result is a single installable app — no terminal, no manual `uvicorn` command.

## Architecture
```
CNC Calc.app / .exe
├── Tauri shell (Rust)          ← manages window + sidecar lifecycle
├── Next.js static files        ← pre-built into frontend/out/, served by Tauri
└── run_server (PyInstaller)    ← FastAPI + uvicorn + engine, bundled Python runtime
        ↑
        spawned on startup, killed on shutdown via tauri-plugin-shell
```

---

## Step 1 — Install PyInstaller

```bash
cd backend
pip install pyinstaller
```

Add to `pyproject.toml` dev dependencies:
```toml
[tool.poetry.dev-dependencies]
pyinstaller = ">=6.0"
```

---

## Step 2 — Verify the Entry Point

`backend/run_server.py` already exists. Confirm it runs correctly before packaging:

```bash
cd backend
python run_server.py
# Should start uvicorn at http://127.0.0.1:8000
```

---

## Step 3 — Create the PyInstaller Spec

Create `backend/run_server.spec`. A spec file (rather than CLI flags) is needed because the engine package has nested sub-packages that PyInstaller won't discover automatically.

```python
# backend/run_server.spec
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all engine sub-packages explicitly
hidden_imports = (
    collect_submodules('engine')
    + collect_submodules('app')
    + collect_submodules('models')
    + collect_submodules('services')
    + collect_submodules('schemas')
    + ['uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto',
       'uvicorn.protocols', 'uvicorn.protocols.http',
       'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets',
       'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan',
       'uvicorn.lifespan.on', 'aiosqlite', 'sqlalchemy.dialects.sqlite',
       'greenlet']
)

a = Analysis(
    ['run_server.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include alembic migrations so the DB can be initialised at runtime
        ('alembic', 'alembic'),
        ('alembic.ini', '.'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['psycopg2', 'asyncpg', 'redis', 'boto3', 'botocore'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='run_server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,       # keep True during development for log visibility
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Build it:
```bash
cd backend
pyinstaller run_server.spec --distpath dist --workpath build/pyinstaller
```

Output: `backend/dist/run_server` (macOS/Linux) or `backend/dist/run_server.exe` (Windows).

**Test the binary independently before wiring it into Tauri:**
```bash
./backend/dist/run_server
curl http://127.0.0.1:8000/api/health
```

---

## Step 4 — Register the Sidecar in `tauri.conf.json`

Tauri requires the binary to be listed in `bundle.externalBin`. The path is relative to `src-tauri/`.

```json
// src-tauri/tauri.conf.json
"bundle": {
  "externalBin": [
    "../backend/dist/run_server"
  ]
}
```

Tauri will copy the binary into the app bundle and apply platform-specific suffixes automatically (e.g. `run_server-aarch64-apple-darwin`).

> **Cross-platform note:** PyInstaller produces platform-native binaries. You must build on each target platform (macOS, Windows, Linux) separately — or use CI (e.g. GitHub Actions matrix) for cross-platform releases.

---

## Step 5 — Spawn and Kill the Sidecar from Rust

Update `src-tauri/src/main.rs` to manage the sidecar lifecycle:

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use tauri::{Manager, State};
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandChild;

struct SidecarHandle(Mutex<Option<CommandChild>>);

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(SidecarHandle(Mutex::new(None)))
        .setup(|app| {
            let sidecar_cmd = app.shell().sidecar("run_server")?;
            let (_rx, child) = sidecar_cmd.spawn()?;

            // Store the child handle so we can kill it on shutdown
            *app.state::<SidecarHandle>().0.lock().unwrap() = Some(child);

            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::Destroyed = event {
                let handle: State<SidecarHandle> = window.state();
                if let Some(child) = handle.0.lock().unwrap().take() {
                    let _ = child.kill();
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## Step 6 — Database Initialisation at Runtime

The SQLite database (`cnccalc.db`) and seed data won't exist on a fresh install. The sidecar needs to create and seed the DB on first launch.

**Option A (simpler) — auto-migrate + seed in `run_server.py`:**

```python
# backend/run_server.py  (updated)
import asyncio
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, Base, AsyncSessionLocal
from scripts.seed_data import seed_data

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()   # idempotent — skips rows that already exist

import uvicorn

if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, log_config=None)
```

**Option B — run Alembic migrations at startup** (preferred if schema is still evolving):

```python
import subprocess
subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=backend_dir)
```

Note: Alembic must be included in the PyInstaller bundle (`datas` and `hiddenimports`) for this to work.

---

## Step 7 — Full Build Pipeline

Add a build script at the root to orchestrate the full production build:

```bash
#!/usr/bin/env bash
# scripts/build-desktop.sh
set -e

echo "==> Building Python sidecar..."
cd backend
pyinstaller run_server.spec --distpath dist --workpath build/pyinstaller
cd ..

echo "==> Building Tauri app..."
cargo tauri build

echo "==> Done. Installer at: src-tauri/target/release/bundle/"
```

Add to root `package.json`:
```json
"build:desktop": "bash scripts/build-desktop.sh"
```

---

## Verification Checklist

- [ ] `python run_server.py` starts cleanly, `GET /api/health` → 200
- [ ] `./backend/dist/run_server` starts cleanly (no Python on PATH), `GET /api/health` → 200
- [ ] `cargo tauri build` completes without errors
- [ ] Installed `.app` / `.exe` launches without any terminal window
- [ ] ScenarioBuilder dropdowns populate (materials, machines, policies)
- [ ] Full recommendation round-trip works end-to-end from inside the packaged app
- [ ] Closing the window kills the `run_server` process (verify via Activity Monitor / Task Manager)

---

## Known Constraints

| Constraint | Detail |
|---|---|
| Platform-specific builds | Must build on each OS; no cross-compilation for Python bundles |
| Binary size | Expect ~80–150 MB for the Python runtime + deps |
| Startup latency | Uvicorn takes ~1–3 s to start; the frontend should show a loading state until `/api/health` responds |
| `console=True` in spec | Change to `console=False` for release to hide the terminal window on Windows |
| DB location | SQLite file will be written to the binary's working directory; for production, use `tauri::api::path::app_data_dir()` passed as an env var to the sidecar |

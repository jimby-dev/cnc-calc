"""
Entry point for PyInstaller bundling.
Runs the FastAPI backend as a standalone executable for Tauri sidecar use.
"""
import sys
from pathlib import Path

# Ensure backend directory is on sys.path (same as main.py)
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_config=None,
    )

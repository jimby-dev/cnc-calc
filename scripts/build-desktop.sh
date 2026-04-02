#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# build-desktop.sh — Full production build for the CNC Calc desktop app.
#
# Usage (from repo root):
#   bash scripts/build-desktop.sh
#   npm run build:desktop
#
# Prerequisites:
#   - Python venv active with PyInstaller installed  (pip install pyinstaller)
#   - Rust + Cargo installed                         (https://rustup.rs)
#   - Tauri CLI installed                            (cargo install tauri-cli)
#   - Node deps installed                            (npm install)
# ---------------------------------------------------------------------------
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"

# ---------------------------------------------------------------------------
# 1. Build the Python sidecar
# ---------------------------------------------------------------------------
echo ""
echo "==> [1/2] Building Python sidecar (PyInstaller)..."
echo "    Backend: $BACKEND_DIR"

cd "$BACKEND_DIR"

# Sanity-check that PyInstaller is available.
if ! python -m PyInstaller --version &>/dev/null; then
  echo "ERROR: PyInstaller not found. Run:  pip install pyinstaller"
  exit 1
fi

python -m PyInstaller run_server.spec \
  --distpath dist \
  --workpath build/pyinstaller \
  --noconfirm

SIDECAR="$BACKEND_DIR/dist/run_server"
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32" ]]; then
  SIDECAR="${SIDECAR}.exe"
fi

if [[ ! -f "$SIDECAR" ]]; then
  echo "ERROR: Expected sidecar binary not found at $SIDECAR"
  exit 1
fi

echo "    Sidecar built: $SIDECAR"

# Quick smoke-test: launch sidecar, wait for it to bind, hit /api/health.
echo "    Smoke-testing sidecar..."
"$SIDECAR" &
SIDECAR_PID=$!

MAX_WAIT=20
for i in $(seq 1 $MAX_WAIT); do
  if curl -sf http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    echo "    /api/health OK (after ${i}s)"
    break
  fi
  if [[ $i -eq $MAX_WAIT ]]; then
    echo "ERROR: sidecar did not respond within ${MAX_WAIT}s"
    kill "$SIDECAR_PID" 2>/dev/null || true
    exit 1
  fi
  sleep 1
done

kill "$SIDECAR_PID" 2>/dev/null || true
wait "$SIDECAR_PID" 2>/dev/null || true

# ---------------------------------------------------------------------------
# 2. Build the Tauri app (compiles Rust shell + bundles frontend + sidecar)
# ---------------------------------------------------------------------------
echo ""
echo "==> [2/2] Building Tauri app..."
cd "$REPO_ROOT"

cargo tauri build

BUNDLE_DIR="src-tauri/target/release/bundle"
echo ""
echo "==> Build complete!"
echo "    Installer(s) in: $REPO_ROOT/$BUNDLE_DIR"
ls "$BUNDLE_DIR" 2>/dev/null || true

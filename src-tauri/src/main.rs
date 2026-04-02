// Prevents an additional console window on Windows in release builds.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::sync::Mutex;
use tauri::{Manager, State};
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandChild;

/// Holds the sidecar process handle so we can kill it on shutdown.
struct SidecarHandle(Mutex<Option<CommandChild>>);

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(SidecarHandle(Mutex::new(None)))
        .setup(|app| {
            // Resolve the OS-appropriate app-data directory and create it if
            // it doesn't exist yet.  This is where the SQLite DB will live.
            let data_dir = app
                .path()
                .app_data_dir()
                .expect("failed to resolve app data directory");

            std::fs::create_dir_all(&data_dir)
                .expect("failed to create app data directory");

            let db_path = data_dir.join("cnccalc.db");

            // Spawn the Python sidecar, passing the DB path via env var so
            // the backend writes its SQLite file to the correct location.
            let sidecar_cmd = app
                .shell()
                .sidecar("run_server")
                .expect("run_server sidecar not found — did you run PyInstaller?")
                .env("CNC_DB_PATH", db_path.to_string_lossy().as_ref());

            let (_rx, child) = sidecar_cmd
                .spawn()
                .expect("failed to spawn run_server sidecar");

            // Store the handle for cleanup on shutdown.
            *app.state::<SidecarHandle>().0.lock().unwrap() = Some(child);

            Ok(())
        })
        .on_window_event(|window, event| {
            // Kill the sidecar when the last window closes.
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

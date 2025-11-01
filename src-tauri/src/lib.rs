// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

use std::{
    path::PathBuf,
    process::{Child, Command},
    sync::{Arc, Mutex},
};

use tauri::WindowEvent;

fn start_server() -> Child {
    let mut is_embed: bool = false;
    let mut python: PathBuf = std::env::current_exe().expect("获取可执行文件路径时出错");
    python = python.parent().unwrap().to_path_buf();

    let mut embed_python = python.clone();

    python.push(r"..\..\..\src-python\.venv\Scripts\python.exe");
    if !python.exists() {
        embed_python.push(r"python\python.exe");
        python = embed_python;
        is_embed = true;
    }

    println!("python: {}", python.display());

    let mut cmd = Command::new(python.clone().into_os_string());
    if is_embed {
        cmd.env("PYTHONPATH", python.parent().unwrap().join("Lib"));
    };

    let handle = cmd
        .args(["-m", "handyapi.main"])
        .spawn()
        .expect("failed to execute process");

    handle
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let handle = Arc::new(Mutex::new(start_server()));
    let handle_cloned = handle.clone();

    tauri::Builder::default()
        .on_window_event(move |_win, event| match event {
            WindowEvent::CloseRequested { .. } => {
                println!("kill server thread.");
                if let Ok(mut child) = handle_cloned.lock() {
                    child.kill().expect("command couldn't be killed");
                } else {
                    println!("failed to lock handle for killing");
                }
                println!("application exit");
            }
            _ => {}
        })
        .plugin(tauri_plugin_opener::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

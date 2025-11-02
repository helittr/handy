// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/

use std::{
    os::windows::process::CommandExt,
    path::PathBuf,
    process::{Child, Command},
};

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
        cmd.env(
            "PYTHONPATH",
            python.parent().unwrap().join("Lib/site-packages"),
        );
    };

    const CREATE_NO_WINDOW: u32 = 0x08000000;
    let handle = cmd
        .creation_flags(CREATE_NO_WINDOW)
        .args(["-m", "handyapi"])
        .spawn()
        .expect("failed to execute process");

    handle
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let mut handle = start_server();

    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run_return(|_app_handle, _run_event| {});

    println!("kill server thread.");
    handle.kill().expect("command couldn't be killed");
    println!("application exit");
}

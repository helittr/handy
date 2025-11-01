"""ADB配置模块"""
from typing import Optional
from pathlib import Path
from .models.globalSettingsModel import GlobalSettings
from .models.smSettingsModel import ScriptManagerSettings

GLOBAL_CONFIG_FILE = Path.home() / ".handy" / "config.json"

globalSettings: Optional[GlobalSettings] = None

# "https://www.python.org/ftp/python/3.13.6/python-3.13.6-embed-amd64.zip"

def get_global_settings() -> GlobalSettings:
    """获取全局设置"""
    global globalSettings

    if globalSettings is None:
        if not GLOBAL_CONFIG_FILE.exists():
            # 如果配置文件不存在，创建默认配置
            GLOBAL_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            globalSettings = GlobalSettings()
            with GLOBAL_CONFIG_FILE.open("w", encoding="utf-8") as f:
                f.write(globalSettings.model_dump_json(indent=4))
        else:
            # 从配置文件加载设置
            with GLOBAL_CONFIG_FILE.open("r", encoding="utf-8") as f:
                globalSettings = GlobalSettings.model_validate_json(f.read())

    return globalSettings

def get_script_manager_settings() -> ScriptManagerSettings:
    """获取脚本管理器设置"""
    return get_global_settings().scriptManager

def save_global_settings(settings: GlobalSettings):
    """保存全局设置"""
    global globalSettings

    globalSettings = settings
    with GLOBAL_CONFIG_FILE.open("w", encoding="utf-8") as f:
        f.write(globalSettings.model_dump_json(indent=4))

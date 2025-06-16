"""日志工具模块"""

import time
from pathlib import Path
from ..config import settings


def get_log_path(script_id: int, script_name: str) -> Path:
    """获取日志文件路径"""
    timestamp = int(time.time())
    return settings.LOG_DIR / f"{script_id}-{script_name}-{timestamp}.log"


def setup_logging():
    """初始化日志配置"""
    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)

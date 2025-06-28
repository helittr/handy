"""ADB配置模块"""

import sys
import logging

from pathlib import Path

# 日志配置
LOG_DIR = Path.home() / "handyApi/scripts/logs/"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 脚本配置
USER_SCRIPTS_JSON = Path.home() / "handyApi/scripts/scripts.json"


SCRIPTS_JSON = (
    USER_SCRIPTS_JSON
    if USER_SCRIPTS_JSON.exists()
    else Path(__file__).parent.parent.joinpath("scripts/scripts.json")
)

# API配置
API_PREFIX = "/adb"
API_TAGS = ["ADB"]

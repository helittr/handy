from pathlib import Path
# from typing import Literal
from pydantic import BaseModel, Field


# 日志配置
LOG_DIR = Path.home() / ".handy/scripts/logs/"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 脚本配置
USER_SCRIPTS_JSON = Path.home() / ".handy/scripts/scripts_package.json"

SCRIPTS_JSON = (
    USER_SCRIPTS_JSON
    if USER_SCRIPTS_JSON.exists()
    else Path(__file__).parent.parent.joinpath("scripts/scripts_package.json")
)

class ScriptManagerSettings(BaseModel):
    """脚本管理器设置模型"""

    scriptPath: str = Field(default=str(SCRIPTS_JSON), description="脚本存储路径")
    logPath: str = Field(default=LOG_DIR, description="日志存储路径")
    scriptPackages: list[Path] = Field(default=[Path(SCRIPTS_JSON)], description="脚本包列表")

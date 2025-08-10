from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime

from .smSettingsModel import ScriptManagerSettings


class GlobalSettings(BaseModel):
    """全局设置模型"""

    theme: Literal["dark", "light"] = Field(default="dark", description="主题")
    lastUpdate: float = Field(default_factory=lambda: datetime.now().timestamp())

    scriptManager: ScriptManagerSettings = Field(default_factory=ScriptManagerSettings)

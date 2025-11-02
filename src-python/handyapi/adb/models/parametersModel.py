"""ADB脚本参数类型定义模块"""

from typing import Literal as L, List, Annotated
from pydantic import BaseModel, Field


class InputParameter(BaseModel):
    """输入参数配置"""

    name: str
    type: L["input"]
    default: str
    label: str
    required: bool = False
    description: str

    def check_value(self, value: str) -> bool:
        if not isinstance(value, str):
            return False
        return True


class SelectOption(BaseModel):
    """选择项配置"""

    label: str
    value: str


class SelectParameter(BaseModel):
    """选择参数配置"""

    name: str
    type: L["select"]
    default: str | List[str] = Field(default="", description="默认选项")
    multiple: bool = False
    label: str
    description: str
    required: bool = True
    options : Annotated[List[SelectOption], Field()] = Field(default_factory=list)

    def check_value(self, option: str | List[str]) -> bool:

        if self.multiple and isinstance(option, list):
            return all(opt in [opt.value for opt in self.options] for opt in option)

        return option in [opt.value for opt in self.options]


class SwitchParameter(BaseModel):
    """开关参数配置"""

    type: L["switch"]
    name: str
    required: bool = True
    label: str
    description: str
    default: bool = False

    def check_value(self, value: bool) -> bool:
        return isinstance(value, bool)

"""ADB脚本参数类型定义模块"""

from typing import Literal as L, List, Any
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class InputParameter(BaseModel):
    """输入参数配置"""

    name: str
    type: L["input"]
    default: str
    label: str
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
    default: str
    label: str
    description: str
    required: bool = True
    options: List[SelectOption] = Field(default_factory=list)

    def check_value(self, option: str) -> bool:
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

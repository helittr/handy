"""ADB脚本参数模型"""

from typing import Any, Literal, Optional, Dict
from pydantic import BaseModel, Field


ParameterType = Literal["input", "select", "switch"]


class InputParameter(BaseModel):
    """输入参数模型"""

    name: str
    type: ParameterType
    default: Optional[Any] = None
    description: Optional[str] = None
    required: bool = True

    def check_value(self, value: Any) -> bool:
        """验证输入参数值"""
        if self.required and value is None:
            return False
        return True


class SelectOption(BaseModel):
    """选择参数选项模型"""

    label: str
    value: str


class SelectParameter(BaseModel):
    """选择参数模型"""

    name: str
    type: ParameterType
    options: list[SelectOption]
    default: Optional[Any] = None
    description: Optional[str] = None
    required: bool = True

    def check_value(self, value: Any) -> bool:
        """验证选择参数值"""
        if self.required and value is None:
            return False
        return value in [option.value for option in self.options]


class SwitchParameter(BaseModel):
    """开关参数模型"""

    name: str
    type: ParameterType
    default: bool = False
    description: Optional[str] = None
    required: bool = False

    def check_value(self, value: Any) -> bool:
        """验证开关参数值"""
        return isinstance(value, bool)

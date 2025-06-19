"""ADB脚本参数模型"""

from abc import ABC, abstractmethod
from typing import Any, Literal, Optional, Dict
from pydantic import BaseModel, Field


class BaseParameter(BaseModel, ABC):
    name: str
    label: str
    type: str
    default: Optional[Any]
    description: str = ""
    required: bool = True

    @abstractmethod
    def check_value(self, value: Any) -> bool:
        pass


class InputParameter(BaseParameter):
    """输入参数模型"""

    type: Literal["input"]
    default: Optional[str]

    def check_value(self, value: Any) -> bool:
        """验证输入参数值"""
        if self.required and value is None:
            return False
        return True


class SelectOption(BaseModel):
    """选择参数选项模型"""

    label: str
    value: str


class SelectParameter(BaseParameter):
    """选择参数模型"""

    type: Literal["select"]
    default: Optional[str]
    options: list[SelectOption] = Field(default_factory=list)

    def check_value(self, value: Any) -> bool:
        """验证选择参数值"""
        if self.required and value is None:
            return False
        return value in [option.value for option in self.options]


class SwitchParameter(BaseParameter):
    """开关参数模型"""

    type: Literal["switch"]
    default: Optional[bool]

    def check_value(self, value: Any) -> bool:
        """验证开关参数值"""
        return isinstance(value, bool)

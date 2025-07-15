"""ADB脚本数据模型模块"""

import typing as t
from pathlib import Path
from enum import Enum, auto

from pydantic import BaseModel, RootModel, Field, AfterValidator
from typing_extensions import Annotated

from .parameters import InputParameter, SelectParameter, SwitchParameter


class GlobalId:
    """全局ID生成器"""

    _next_id: t.ClassVar[int] = 1

    @classmethod
    def get_next_id(cls) -> int:
        current_id = cls._next_id
        cls._next_id += 1
        return current_id


def validate_path(value: str, info: t.Any) -> str:
    """验证并解析路径"""
    context = info.context
    if not context or "source" not in context:
        raise ValueError("Source context is required for path validation.")

    source = context["source"]
    if not Path(value).is_absolute():
        value = str(Path(source).parent.joinpath(value))
    return value


type IdType = int


class ScriptInfo(BaseModel):
    """脚本信息模型"""

    id: IdType = Field(default_factory=GlobalId.get_next_id)
    name: str
    type: t.Literal["winpowershell", "powershell"]
    path: Annotated[str, AfterValidator(validate_path)]
    label: str
    description: str
    parameters: t.List[
        t.Annotated[
            InputParameter | SelectParameter | SwitchParameter,
            Field(default_factory=list, discriminator="type"),
        ]
    ]


class GroupInfo(BaseModel):
    """脚本组信息模型"""

    id: IdType = Field(default_factory=GlobalId.get_next_id)
    name: str
    type: t.Literal["scriptgroup"]
    label: str
    description: str
    children: t.List[
        Annotated[
            "GroupInfo|ScriptInfo", Field(default_factory=list, discriminator="type")
        ]
    ]


class RootGroup(RootModel):
    """根组模型"""

    root: t.List[
        Annotated[
            "GroupInfo|ScriptInfo", Field(default_factory=list, discriminator="type")
        ]
    ]

    def __iter__(self):
        for item in self.root:
            yield item.id, item


class ExecuteParam(RootModel):
    """脚本执行参数模型"""

    root: t.Dict[str, str | bool]


class ScriptStatus(Enum):
    """脚本状态枚举"""

    PRE = auto()
    RUNNING = auto()
    FINISH = auto()
    TERMINATED = auto()

class ManagerInfo(BaseModel):

    logpath: str

"""ADB脚本数据模型模块"""

import typing as t
from pathlib import Path
from enum import Enum, auto

from pydantic import BaseModel, RootModel, Field, AfterValidator
from typing_extensions import Annotated

from .parametersModel import InputParameter, SelectParameter, SwitchParameter


class GlobalId:
    """全局ID生成器"""

    _next_id: t.ClassVar[int] = 1

    @classmethod
    def get_next_id(cls) -> int:
        current_id = cls._next_id
        cls._next_id += 1
        return current_id


def validate_path(value: str|None, info: t.Any) -> str|None:
    """验证并解析路径"""
    if value is None:
        return value

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

    id: Annotated[IdType, Field()] = Field(default_factory=GlobalId.get_next_id)
    name: str
    type: t.Literal["winpowershell", "powershell", "python"]
    path: Annotated[str, AfterValidator(validate_path)]
    newconsole: bool = False
    label: str
    description: str
    parameters: t.List[
        t.Annotated[
            InputParameter | SelectParameter | SwitchParameter,
            Field(discriminator="type"),
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
            "GroupInfo|ScriptInfo", Field(discriminator="type")
        ]
    ] = Field(default_factory=list)

class RootGroup(RootModel):
    """根组模型"""

    root: t.List[
        Annotated[
            "GroupInfo|ScriptInfo", Field(discriminator="type")
        ]
    ] = Field(default_factory=list)

    def iter(self) -> t.Iterator[t.Tuple[IdType, t.Union[GroupInfo, ScriptInfo]]]:
        for item in self.root:
            yield (item.id, item)

class ScriptPackage(BaseModel):
    """脚本包模型"""

    id: IdType
    name: str
    label: str
    description: str
    install: str
    python: Annotated[str|None, AfterValidator(validate_path)]
    scripts: RootGroup


class ExecuteParam(RootModel):
    """脚本执行参数模型"""

    root: t.Dict[str, str | bool | t.List[str]]


class ScriptStatus(Enum):
    """脚本状态枚举"""

    PRE = auto()
    RUNNING = auto()
    FINISH = auto()
    TERMINATED = auto()

class ManagerInfo(BaseModel):

    logpath: str

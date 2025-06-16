"""验证工具模块"""

from pathlib import Path
from typing import Any
from ..config import settings


def validate_path(value: str, source: Path) -> str:
    """验证并解析路径"""
    if not Path(value).is_absolute():
        value = str(source.parent.joinpath(value))
    return value


def validate_parameters(parameters: dict, script_info) -> None:
    """验证执行参数"""
    for param in script_info.parameters:
        if param.name not in parameters.keys():
            raise ValueError(f"Missing required parameter: {param.name}")

        if not param.check_value(parameters[param.name]):
            raise ValueError(
                f"Invalid value for parameter '{param.name}': {parameters[param.name]}"
            )

"""ADB脚本工厂模块"""

import typing as t
from ..utils.validator import validate_parameters
from .baseScript import BaseScript
from ..models.script import ScriptInfo, ExecuteParam


class ScriptFactory:
    """脚本工厂类"""

    _registry: t.ClassVar[t.Dict[str, t.Type[BaseScript]]] = {}

    @classmethod
    def register_script_type(cls, script_type: str):
        """注册脚本类型装饰器"""

        def decorate(script_class: t.Type[BaseScript]):
            cls._registry[script_type] = script_class
            return script_class

        return decorate

    @classmethod
    def create_script(cls, script_info: ScriptInfo, logfile: str) -> BaseScript:
        """创建脚本实例"""
        if script_info.type == "scriptgroup":
            raise ValueError("Script groups cannot be instantiated directly")

        if script_class := cls._registry.get(script_info.type):
            return script_class(script_info, logfile)

        raise ValueError(f"Unsupported script type: {script_info.type}")


@ScriptFactory.register_script_type("winpowershell")
class WinPowerShellScript(BaseScript):
    """Windows PowerShell脚本实现类"""

    def _get_cmdline(self, parameters: ExecuteParam):
        validate_parameters(parameters.model_dump(), self.info)
        cmdline = [
            "powershell",
            "-NoLogo",
            "-NonInteractive",
            "-File",
            self.info.path,
        ]

        for param in self.info.parameters:
            if param.name.startswith("-"):
                if (
                    isinstance(parameters.root[param.name], bool)
                    and parameters.root[param.name]
                ):
                    cmdline.append(param.name)
                else:
                    cmdline.append(param.name)

            if isinstance(parameters.root[param.name], str) and len(
                parameters.root[param.name].strip()
            ):
                cmdline.append(parameters.root[param.name].strip())

        return cmdline

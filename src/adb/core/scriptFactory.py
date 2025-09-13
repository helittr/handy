"""ADB脚本工厂模块"""

import typing as t
from ..utils.validator import validate_parameters
from .baseScript import BaseScript
from ..models.scriptModel import ScriptInfo, ExecuteParam


class ScriptFactory:
    """脚本工厂类"""

    _registry: t.ClassVar[t.Dict[str, t.Type[BaseScript]]] = {}
    _exe_path: t.Dict[str, str] = {}

    @classmethod
    def set_executable_path(cls, script_type: str, path: str) -> None:
        """设置可执行文件路径"""
        if script_type in cls._registry.keys():
            cls._exe_path[script_type] = path
        else:
            raise ValueError(f"Unsupported script type: {script_type}")

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
            return script_class(script_info, logfile, cls._exe_path.get(script_info.type))

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
            "-ExecutionPolicy",
            "remoteSigned",
            "-File",
            self.info.path,
        ]

        for param in self.info.parameters:
            name = param.name
            value = parameters.root[name]
            if name.startswith("-"):
                if isinstance(value, bool):
                    if value:
                        cmdline.append(name)
                elif isinstance(value, str):
                    if value.strip() != '':
                        cmdline.append(name)

            if isinstance(value, str) and len(
                value.strip()
            ):
                cmdline.append(value.strip())

            if isinstance(value, list):
                for v in value:
                    if v.strip():
                        cmdline.append(v.strip())

        return cmdline

@ScriptFactory.register_script_type("powershell")
class PowerShellScript(BaseScript):
    """PowerShell脚本实现类"""

    def _get_cmdline(self, parameters: ExecuteParam):
        validate_parameters(parameters.model_dump(), self.info)
        cmdline = [
            "pwsh",
            "-NoLogo",
            "-NonInteractive",
            "-ExecutionPolicy",
            "remoteSigned",
            "-File",
            self.info.path,
        ]

        for param in self.info.parameters:
            name = param.name
            value = parameters.root[name]

            if name.startswith("-"):
                if isinstance(value, bool):
                    if value:
                        cmdline.append(name)
                elif isinstance(value, str):
                    if value.strip() != '':
                        cmdline.append(name)

            if isinstance(value, str) and len(
                value.strip()
            ):
                cmdline.append(value.strip())

        return cmdline

@ScriptFactory.register_script_type("python")
class PythonScript(BaseScript):
    """Python脚本实现类"""

    def _get_cmdline(self, parameters: ExecuteParam):
        validate_parameters(parameters.model_dump(), self.info)
        cmdline = [
            self.exec if self.exec else "python",
            self.info.path,
        ]

        for param in self.info.parameters:
            name = param.name
            value = parameters.root[name]

            if name.startswith("-"):
                if isinstance(value, bool):
                    if value:
                        cmdline.append(name)
                elif isinstance(value, str):
                    if value.strip() != '':
                        cmdline.append(name)

            if isinstance(value, str) and len(
                value.strip()
            ):
                cmdline.append(value.strip())

        return cmdline
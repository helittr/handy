"""ADB脚本管理模块


提供脚本管理功能，包括：
- 脚本参数定义和验证
- 脚本执行管理
- 脚本组管理
"""

import os
import time
import subprocess
import typing as t
from io import BufferedWriter
from abc import abstractmethod
from enum import Enum, auto
from pathlib import Path

from pydantic import BaseModel, RootModel, Field, AfterValidator
from typing_extensions import Annotated


# Define the types of parameters that can be used in the scripts
class InputParameter(BaseModel):
    """Represents an input parameter configuration for scripts.

    Attributes:
        name: The parameter name
        type: Literal type "input"
        default: Default value
        label: Display label
        description: Parameter description
    """

    name: str
    type: t.Literal["input"]
    default: str
    label: str
    description: str

    def check_value(self, value: str) -> bool:
        """Checks if the provided value is valid for this parameter."""
        if not isinstance(value, str):
            return False
        # Additional validation logic can be added here
        return True


class SelectOption(BaseModel):
    """Represents a selectable option for SelectParameter.

    Attributes:
        label: Display text for the option
        value: Internal value of the option
    """

    label: str
    value: str


class SelectParameter(BaseModel):
    """Represents a selection parameter with multiple options.

    Attributes:
        name: The parameter name
        type: Literal type "select"
        default: Default selected value
        label: Display label
        description: Parameter description
        options: List of available options
    """

    name: str
    type: t.Literal["select"]
    default: str
    label: str
    description: str
    required: bool = True
    options: t.List[SelectOption] = Field(default_factory=list)

    def check_value(self, option: str) -> bool:
        """Checks if the provided option is valid for this parameter."""
        return option in [opt.value for opt in self.options]


class SwitchParameter(BaseModel):
    """Represents a switch parameter."""

    type: t.Literal["switch"]
    name: str
    required: bool = True
    label: str
    description: str
    default: bool = False

    def check_value(self, value: bool) -> bool:
        """Checks if the provided value is valid for this parameter."""
        return isinstance(value, bool)


# Define the script information
class GlobalId:
    """Generates unique sequential IDs for scripts and groups.

    Class Attributes:
        _next_id: The next available ID number
    """

    _next_id: t.ClassVar[int] = 1

    @classmethod
    def get_next_id(cls) -> int:
        """Generate and return the next available sequential ID.

        Returns:
            int: The next available ID
        """
        current_id = cls._next_id
        cls._next_id += 1
        return current_id


def validate_path(value: str, info: t.Any) -> str:
    """验证并解析路径

    Args:
        value: 要验证的路径
        info: ValidationInfo 对象，包含验证上下文

    Returns:
        str: 验证后的绝对路径
    """
    context = info.context
    if not context or "source" not in context:
        raise ValueError("Source context is required for path validation.")

    source = context["source"]
    if not Path(value).is_absolute():
        value = str(Path(source).parent.joinpath(value))

    return value


type IdType = int


class ScriptInfo(BaseModel):
    """Represents a script with metadata and parameters."""

    id: IdType = Field(default_factory=GlobalId.get_next_id)
    name: str
    type: t.Literal["winpowershell"]
    path: Annotated[str, AfterValidator(validate_path)]
    label: str
    description: str
    parameters: t.List[
        Annotated[
            InputParameter | SelectParameter | SwitchParameter,
            Field(default_factory=list, discriminator="type"),
        ]
    ]


# Define the script group information
class GroupInfo(BaseModel):
    """Represents a group of scripts with metadata."""

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
    """Represents the root group of scripts."""

    root: t.List[
        Annotated[
            "GroupInfo|ScriptInfo", Field(default_factory=list, discriminator="type")
        ]
    ]

    def __iter__(self):
        """Iterate over items in the root group yielding (id, item) pairs.

        Yields:
            Tuple[int, Union[GroupInfo, ScriptInfo]]: ID and item pairs
        """
        for item in self.root:
            yield item.id, item


class ExecuteParam(RootModel):
    """the parameter of script to execute"""

    root: t.Dict[str, str | bool]


class ScriptStatus(Enum):
    """the current status of script"""

    # UNKNOWN = auto()
    PRE = auto()
    RUNNING = auto()
    FINISH = auto()


class BaseScript:
    """Base class for scripts, can be extended for specific script types."""

    def __init__(self, script_info: ScriptInfo, logfile: str):
        self.taskid: IdType = time.time_ns() // 1000
        self.info: ScriptInfo = script_info
        self.status: ScriptStatus = ScriptStatus.PRE
        self.logfile: Path = Path(logfile)
        self.out: t.Optional[BufferedWriter] = None
        self.process: t.Optional[subprocess.Popen] = None
        self.createtime: float = time.time()
        self.starttime: float | None = None
        self.endtime: float | None = None

        if self.logfile.exists():
            raise FileExistsError(f"{self.logfile.absolute()} is already exist")

    def validate_parameters(self, parameters: ExecuteParam) -> None:
        """Validates the provided parameters against the script's expected parameters."""
        parameters = parameters.model_dump()
        for param in self.info.parameters:
            if param.name not in parameters.keys():
                raise ValueError(f"Missing required parameter: {param.name}")

            if not param.check_value(parameters[param.name]):
                raise ValueError(
                    f"Invalid value for parameter '{param.name}': {parameters[param.name]}"
                )

    @abstractmethod
    def _get_cmdline(self, parameters: ExecuteParam) -> t.List[str]:
        raise NotImplementedError

    def execute(self, parameters: ExecuteParam) -> None:
        """execute script"""
        print(f"Running script: script information:{self.info} ")

        self.validate_parameters(parameters)
        print(f"Executing script '{self.info.name}' with parameters: {parameters}")

        if self.status != ScriptStatus.PRE:
            raise SyntaxError(f"script status exception,{self.status}")
        self.starttime = time.time()
        self.status = ScriptStatus.RUNNING

        self.out = self.logfile.open(mode="wb")
        self.process = subprocess.Popen(self._get_cmdline(parameters), stdout=self.out)

    def get_status(self) -> ScriptStatus:
        """get script status"""

        if self.process and self.process.poll() is not None:
            print(
                f"Script '{self.info.name}' is finished code {self.process.returncode}"
            )
            self.status = ScriptStatus.FINISH
            self.endtime = time.time()
            self.out.close()
            self.process = None

        return self.status

    def get_log(self, pos: int, max_size: int) -> bytes:
        """get command log"""
        try:
            with self.logfile.open("rb") as f:
                try:
                    f.flush()
                    f.seek(pos, os.SEEK_SET)
                except ValueError as e:
                    print(f"Invalid position: {pos}, error: {e}")
                    return b""
                return f.read(max_size)
        except FileNotFoundError:
            print(f"Log file not found: {self.logfile.absolute()}")
            return b""


class ScriptFactory:
    """Factory class to create script instances based on their type."""

    # Registry mapping script types to their implementation classes
    _registry: t.ClassVar[t.Dict[str, t.Type[BaseScript]]] = {
        # "winpowershell": WinPowerShellScript
    }

    @classmethod
    def register_script_type(cls, script_type: str):
        """Register a new script type with its implementation class."""

        def decorate(script_class: t.Type[BaseScript]):
            cls._registry[script_type] = script_class
            return script_class

        return decorate

    @classmethod
    def create_script(cls, script_info: ScriptInfo, logfile: str) -> t.Type[BaseScript]:
        """Create a script instance based on the script type.

        Args:
            script_info: Script metadata and configuration

        Returns:
            Instance of the appropriate script implementation class

        Raises:
            ValueError: For unsupported script types or script groups
        """
        if script_info.type == "scriptgroup":
            raise ValueError("Script groups cannot be instantiated directly")

        if script_class := cls._registry.get(script_info.type):
            return script_class(script_info, logfile)

        raise ValueError(f"Unsupported script type: {script_info.type}")


@ScriptFactory.register_script_type("winpowershell")
class WinPowerShellScript(BaseScript):
    """Represents a Windows PowerShell script."""

    # def __init__(self, script_info: ScriptInfo, log_path: str):
    #     super().__init__(script_info, log_path)
    #     if self.info.type != "winpowershell":
    #         raise ValueError("Script type must be 'winpowershell' for this class.")

    def _get_cmdline(self, parameters: ExecuteParam):
        parameters = parameters.model_dump()
        cmdline = [
            "powershell",
            "-NoLogo",
            "-NonInteractive",
            "-File",
            self.info.path,
        ] + [
            f"{param.name if param.name.startswith('-') else ''} {'' if isinstance(parameters[param.name], bool) else parameters[param.name]}"
            for param in self.info.parameters
            if param.name in parameters
        ]
        print(cmdline)
        print(self.info.parameters)
        print(parameters)

        return cmdline


class ScriptManager:
    """Manages a collection of scripts and their execution."""

    def __init__(self, source: str):
        """Initializes the script manager from either a RootGroup object or a JSON string."""
        if isinstance(source, str):
            self.source = Path(source)
        else:
            raise TypeError("Source must be a string or a list of strings.")

        self.rootgroup = RootGroup.model_validate_json(
            self.source.read_text(encoding="utf-8"), context={"source": self.source}
        )
        self.task: t.Dict[IdType, t.Type[BaseScript]] = {}

        self.logdir: Path = Path("./tmp/log")
        self.logdir.mkdir(parents=True, exist_ok=True)
        self.lastupdate: float = time.time()

    def find_script_info(self, sid: IdType) -> t.Optional[ScriptInfo]:
        """Find a script by its ID in the script hierarchy.

        Args:
            sid: The script ID to search for

        Returns:
            Optional[ScriptInfo]: The found script or None if not found
        """

        def find_in_group(
            group: t.List[t.Union[ScriptInfo, GroupInfo]], sid: IdType
        ) -> t.Optional[ScriptInfo]:
            """Finds a script by its id."""
            for item in group:
                if isinstance(item, ScriptInfo) and item.id == sid:
                    return item
                elif isinstance(item, GroupInfo):
                    found_script = find_in_group(item.children, sid)
                    if found_script:
                        return found_script
            return None

        for ssid, item in self.rootgroup:
            # print("find item", item, "ID", sid)
            if isinstance(item, ScriptInfo) and ssid == sid:
                return item
            elif isinstance(item, GroupInfo):
                found_script = find_in_group(item.children, sid)
                if found_script:
                    return found_script
        return None

    def execute_script(self, sid: IdType, parameters: ExecuteParam) -> IdType:
        """Executes a script by its ID and returns execution ID.

        Args:
            sid: Script ID to execute
            parameters: Execution parameters

        Returns:
            int: Execution ID (currently returns script ID as placeholder)

        Raises:
            ValueError: If script not found
        """
        scriptinfo = self.find_script_info(sid)
        if scriptinfo:
            task = ScriptFactory.create_script(
                scriptinfo,
                self.logdir.joinpath(f"{sid}-{scriptinfo.name}-{time.time()}.log"),
            )
            self.task[task.taskid] = task
            task.execute(parameters)
            return task.taskid
        else:
            raise ValueError(f"Script '{sid}' not found.")

    def get_script_status(self, sid: IdType) -> ScriptStatus:
        """get script status by id"""
        task = self.task.get(sid)
        if not task:
            return ScriptStatus.PRE
        return task.get_status()

    def get_script_log(self, tid: IdType, pos: int = 0, size: int = 0) -> bytes:
        """get script log by id"""
        task = self.task.get(tid)
        print("get log", task, self.task)
        if task is None:
            raise ValueError(f"Task '{tid}' not found.")
        return task.get_log(pos, size)

    def get_task(self) -> t.Dict[IdType, t.Type[BaseScript]]:
        """get task"""
        return self.task

    def del_task(self, tid: IdType) -> bool:
        """delete task"""
        if tid in self.task:
            if self.task[tid].get_status() == ScriptStatus.RUNNING:
                raise ValueError("Cannot delete running task.")
            del self.task[tid]
            self.lastupdate = time.time()
            return True
        raise ValueError(f"Task '{tid}' not found.")


if __name__ == "__main__":
    # Example usage
    manager = ScriptManager(str(Path(__file__).joinpath("../scripts/scripts.json")))

    manager.execute_script("example", {"param1": "value1", "param2": "option1"})

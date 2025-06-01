import typing as t
from abc import ABC, abstractmethod
from typing_extensions import Annotated
from pathlib import Path

from pydantic import BaseModel, RootModel, Field, field_validator, AfterValidator

import subprocess

# Define the types of parameters that can be used in the scripts


class InputParameter(BaseModel):
    name: str
    type: t.Literal["input"]
    default: str
    label: str
    description: str

    def check_value(self, value: str) -> bool:
        ''' Checks if the provided value is valid for this parameter. '''
        if not isinstance(value, str):
            return False
        if not value:
            return False
        # Additional validation logic can be added here
        return True


class SelectParameter(BaseModel):
    name: str
    type: t.Literal["select"]
    default: str
    label: str
    description: str
    options: t.List[str] = Field(default_factory=list)

    def check_value(self, option: str) -> bool:
        ''' Checks if the provided option is valid for this parameter. '''
        return option in self.options

# Define the script information


class GlobalID:
    _next_id: t.ClassVar[int] = 1

    @classmethod
    def get_next_id(cls) -> int:
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

class ScriptInfo(BaseModel):
    ''' Represents a script with metadata and parameters. '''
    id: int = Field(default_factory=GlobalID.get_next_id)
    name: str
    type: t.Literal["winpowershell"]
    path: Annotated[str, AfterValidator(validate_path)]
    label: str
    description: str
    parameters: t.List[Annotated[InputParameter | SelectParameter, Field(
        default_factory=list, discriminator="type")]]
    

        

# Define the script group information


class GroupInfo(BaseModel):
    ''' Represents a group of scripts with metadata. '''
    id: int = Field(default_factory=GlobalID.get_next_id)
    name: str
    type: t.Literal["scriptgroup"]
    label: str
    description: str
    children: t.List[Annotated['GroupInfo|ScriptInfo',
                               Field(default_factory=list, discriminator="type")]]


class RootGroup(RootModel):
    ''' Represents the root group of scripts. '''
    root:  t.List[Annotated['GroupInfo|ScriptInfo', Field(
        default_factory=list, discriminator="type")]]

    def __iter__(self):
        for item in self.root:
            yield item.name, item

    def __getitem__(self, item):
        return self.root[item]


class BaseScript:
    ''' Base class for scripts, can be extended for specific script types. '''

    def __init__(self, script_info: ScriptInfo):
        self.info: ScriptInfo = script_info

    def validate_parameters(self, parameters: t.Dict[str, str]):
        ''' Validates the provided parameters against the script's expected parameters. '''
        for param in self.info.parameters:
            if param.name not in parameters:
                raise ValueError(
                    f"Missing required parameter: {param.name}")

            if not param.check_value(parameters[param.name]):
                raise ValueError(
                    f"Invalid value for parameter '{param.name}': {parameters[param.name]}")

    @abstractmethod
    def execute(self, parameters: t.Dict[str, str]):
        print(f"Running script: script information:{self.info} ")


class WinPowerShellScript(BaseScript):
    ''' Represents a Windows PowerShell script. '''

    def __init__(self, script_info: ScriptInfo):
        super().__init__(script_info)
        if self.info.type != "winpowershell":
            raise ValueError(
                "Script type must be 'winpowershell' for this class.")

    def execute(self, parameters: t.Dict[str, str]):
        ''' Executes the PowerShell script with the provided parameters. '''
        super().execute(parameters)
        self.validate_parameters(parameters)
        print(
            f"Executing PowerShell script '{self.info.name}' with parameters: {parameters}")
        subprocess.run(["powershell", "-NoLogo","-NonInteractive", "-File", self.info.path] + [
            f"-{param.name} {parameters[param.name]}" for param in self.info.parameters if param.name in parameters], check=True)


class Script:
    ''' Factory class to create script instances based on their type. '''
    def __new__(cls, script_info: ScriptInfo):
        match script_info.type:
            case "scriptgroup":
                raise ValueError(
                    "Cannot create a Script instance from a script group.")
            case "winpowershell":
                return WinPowerShellScript(script_info)
            case _:
                raise ValueError(
                    f"Unsupported script type: {script_info.type}")


class ScriptManager:
    ''' Manages a collection of scripts and their execution. '''

    def __init__(self, source: str):
        ''' Initializes the script manager from either a RootGroup object or a JSON string. '''
        if isinstance(source, str):
            self.source = Path(source)
        else:
            raise TypeError("Source must be a string or a list of strings.")

        self.rootgroup = RootGroup.model_validate_json(self.source.read_text(), context={"source": self.source})

    def find_script(self, script_name: str) -> t.Optional[ScriptInfo]:
        ''' Finds a script by its name. '''
        def find_in_group(group: t.List[t.Union[ScriptInfo, GroupInfo]], script_name: str) -> t.Optional[ScriptInfo]:
            for item in group:
                if isinstance(item, ScriptInfo) and item.name == script_name:
                    return item
                elif isinstance(item, GroupInfo):
                    found_script = find_in_group(item.children, script_name)
                    if found_script:
                        return found_script
            return None

        for name, item in self.rootgroup:
            if isinstance(item, ScriptInfo) and name == script_name:
                return item
            elif isinstance(item, GroupInfo):
                found_script = find_in_group(item.children, script_name)
                if found_script:
                    return found_script
        return None

    def execute_script(self, script_name: str, parameters: t.Dict[str, str]):
        ''' Executes a script by its name. '''
        script = self.find_script(script_name)
        if script:
            script_instance = Script(script)
            script_instance.execute(parameters)
        else:
            raise ValueError(f"Script '{script_name}' not found.")


if __name__ == "__main__":
    # Example usage
    manager = ScriptManager(
        str(Path(__file__).joinpath("../scripts/scripts.json"))
    )

    manager.execute_script(
        "example", {"param1": "value1", "param2": "option1"})

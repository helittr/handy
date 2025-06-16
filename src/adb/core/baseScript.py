"""ADB脚本基础类模块"""

import os
import time
import subprocess
import typing as t
from io import BufferedWriter
from abc import abstractmethod
from pathlib import Path
from abc import ABC

from ..models.script import ScriptInfo, ExecuteParam, ScriptStatus


class BaseScript(ABC):
    """脚本基类"""

    def __init__(self, script_info: ScriptInfo, logfile: str):
        self.taskid: int = time.time_ns() // 1000
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
        """验证执行参数"""
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
        """获取命令行参数(抽象方法)"""
        raise NotImplementedError

    def execute(self, parameters: ExecuteParam) -> None:
        """执行脚本"""
        print(f"Running script: script information:{self.info}")

        self.validate_parameters(parameters)
        print(f"Executing script '{self.info.name}' with parameters: {parameters}")

        if self.status != ScriptStatus.PRE:
            raise SyntaxError(f"script status exception,{self.status}")
        self.starttime = time.time()
        self.status = ScriptStatus.RUNNING

        self.out = self.logfile.open(mode="wb")
        self.process = subprocess.Popen(self._get_cmdline(parameters), stdout=self.out)

    def get_status(self) -> ScriptStatus:
        """获取脚本状态"""
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
        """获取脚本日志"""
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

    def stop(self) -> None:
        """停止正在运行的脚本"""
        if self.status != ScriptStatus.RUNNING:
            raise ValueError(f"Cannot stop script in {self.status} state")

        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

        self.status = ScriptStatus.TERMINATED
        self.endtime = time.time()
        if self.out:
            self.out.close()
        self.process = None
        print(f"Script '{self.info.name}' stopped by user request")

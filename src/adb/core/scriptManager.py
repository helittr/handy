"""ADB脚本管理器模块"""

import logging
import time
import typing as t
from pathlib import Path

from ..config.settings import LOG_DIR
from ..utils.logger import get_log_path
from ..models.script import (
    RootGroup,
    IdType,
    ScriptInfo,
    GroupInfo,
    ExecuteParam,
    ScriptStatus,
)
from .scriptFactory import ScriptFactory
from .baseScript import BaseScript


class ScriptManager:
    """脚本管理器类"""

    def __init__(self, source: str):
        if isinstance(source, str):
            self.source = Path(source)
        else:
            raise TypeError("Source must be a string or a list of strings.")

        self.rootgroup = RootGroup.model_validate_json(
            self.source.read_text(encoding="utf-8"), context={"source": self.source}
        )
        self.rootgroup = RootGroup.model_validate_json(
            self.source.read_text(encoding="utf-8"), context={"source": self.source}
        )
        self.task: t.Dict[IdType, BaseScript] = {}
        self.logdir: Path = LOG_DIR
        self.lastupdate: float = time.time()

    def find_script_info(self, sid: IdType) -> t.Optional[ScriptInfo]:
        """查找脚本信息"""

        def find_in_group(group: t.List[t.Union[ScriptInfo, GroupInfo]], sid: IdType):
            for item in group:
                if isinstance(item, ScriptInfo) and item.id == sid:
                    return item
                elif isinstance(item, GroupInfo):
                    found_script = find_in_group(item.children, sid)
                    if found_script:
                        return found_script
            return None

        for ssid, item in self.rootgroup:
            if isinstance(item, ScriptInfo) and ssid == sid:
                return item
            elif isinstance(item, GroupInfo):
                found_script = find_in_group(item.children, sid)
                if found_script:
                    return found_script
        return None

    def execute_script(self, sid: IdType, parameters: ExecuteParam) -> IdType:
        """执行脚本"""
        scriptinfo = self.find_script_info(sid)
        if scriptinfo:
            task = ScriptFactory.create_script(
                scriptinfo,
                get_log_path(sid, scriptinfo.name),
            )
            self.task[task.taskid] = task
            task.execute(parameters)
            return task.taskid
        else:
            raise ValueError(f"Script '{sid}' not found.")

    def get_script_status(self, sid: IdType) -> ScriptStatus:
        """获取脚本状态"""
        task = self.task.get(sid)
        if not task:
            return ScriptStatus.PRE
        return task.get_status()

    def get_script_log(self, tid: IdType, pos: int = 0, size: int = 0) -> bytes:
        """获取脚本日志"""
        task = self.task.get(tid)
        logging.debug("get log %s %s", task, self.task)
        if task is None:
            raise ValueError(f"Task '{tid}' not found.")
        return task.get_log(pos, size)

    def get_task(self) -> t.Dict[IdType, BaseScript]:
        """获取所有任务"""
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

    def stop_task(self, tid: IdType, force:bool=False) -> bool:
        """停止正在运行的任务"""
        if tid not in self.task:
            raise ValueError(f"Task '{tid}' not found.")

        task = self.task[tid]
        if task.get_status() != ScriptStatus.RUNNING:
            raise ValueError(f"Cannot stop task in {task.get_status()} state")

        if force:
            task.force_stop()
        else:
            task.stop()
        return True

    def reload(self):
        """重新加载脚本"""
        self.rootgroup = RootGroup.model_validate_json(
            self.source.read_text(encoding="utf-8"), context={"source": self.source}
        )
        self.task.clear()
        self.lastupdate = time.time()
        logging.info("ScriptManager reloaded successfully.")
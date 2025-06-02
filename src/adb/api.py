"""
api scriptmanager
"""

import pathlib
from typing import Annotated
# import logging

from fastapi import APIRouter, Path, Response, Query
from . import script_manager as smgr
from .script_manager import ExecuteParam


router = APIRouter(prefix="/adb", tags=["ADB"])

manager = smgr.ScriptManager(
    str(pathlib.Path(__file__).joinpath("../scripts/scripts.json"))
)


@router.get("/commands", summary="获取ADB命令列表")
def get_commands():
    """获取ADB命令列表"""
    return manager.rootgroup


@router.post("/commands/{sid}/execute", summary="执行指定命令")
def exe_command(
    sid: Annotated[int, Path(title="The ID of the command to execute")],
    params: ExecuteParam,
):
    """the api to execute script"""
    print(f"excute command{sid}", params)
    try:
        manager.execute_script(sid, params)
        return {"status": "ok", "code": 0, "execution_id": sid}
    except ValueError as e:
        print("exception", e)
        return {"status": "error", "code": 1, "message": str(e)}


@router.get("/commands/{sid}/status", summary="获取指定命令状态")
def get_status(sid: Annotated[int, Path(title="The ID of the command to get")]):
    """get command status"""
    st = manager.get_script_status(sid)
    return {"id": sid, "code": st}


@router.get("/commands/{sid}/log", summary="获取指定命令日志")
def get_log(
    sid: Annotated[int, Path(title="The ID of the command to get")],
    pos: int = Query(default=0, ge=0, title="The position of the log to get"),
    size: int = Query(default=-1, title="The size of the log to get"),
):
    """get command log"""
    log = manager.get_script_log(sid, pos, size)
    print("response log", log.decode("gb2312", errors="ignore"))
    return Response(content=log, media_type="application/octet-stream")

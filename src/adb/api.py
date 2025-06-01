from fastapi import APIRouter, Path
from . import scriptManager as smgr
from .scriptManager import ExecutParam
import pathlib
from typing import Annotated
import logging


router = APIRouter(prefix="/adb", tags=["ADB"])

manager = smgr.ScriptManager(
    str(pathlib.Path(__file__).joinpath("../scripts/scripts.json"))
)


@router.get("/commands", summary="获取ADB命令列表")
def get_commands():
    """获取ADB命令列表"""
    return manager.rootgroup

@router.post("/commands/{id}/execute", summary="执行指定命令")
def exe_command(
    id: Annotated[int, Path(title="The ID of the command to execute")],
    params: ExecutParam,
):
    print(f"excute command{id}",params)
    try:
        manager.execute_script(id, params)
    except ValueError as e:
        print("exception", e)
        return {"status": "ok", "code": 0, "message": str(e)}
    return {"status": "ok", "code": 0}

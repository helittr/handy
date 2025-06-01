from fastapi import APIRouter
from . import scriptManager as smgr
from pathlib import Path


router = APIRouter(prefix="/adb", tags=["ADB"])

manager = smgr.ScriptManager(
    str(Path(__file__).joinpath("../scripts/scripts.json"))
)


@router.get("/commands", summary="获取ADB命令列表")
def get_commands():
    """获取ADB命令列表"""
    return manager.rootgroup

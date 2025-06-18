"""
api scriptmanager
"""

from typing import Annotated
from fastapi import APIRouter, Path, Response, Query, status
from fastapi.responses import JSONResponse
from ..config.settings import SCRIPTS_JSON
from ..core.scriptManager import ScriptManager
from ..models.script import ExecuteParam

router = APIRouter(prefix="/adb", tags=["ADB"])

manager = ScriptManager(str(SCRIPTS_JSON))


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
        tid = manager.execute_script(sid, params)
        return {"status": "ok", "code": 0, "data": {"taskId": tid}}
    except ValueError as e:
        print("exception", e)
        return JSONResponse(
            content={"code": 400, "status": "error", "message": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/commands/{sid}/status", summary="获取指定命令状态")
def get_status(sid: Annotated[int, Path(title="The ID of the command to get")]):
    """get command status"""
    st = manager.get_script_status(sid)
    return {"id": sid, "status": st}


@router.get("/commands/tasks/{tid}/log", summary="获取任务日志")
def get_log(
    tid: Annotated[int, Path(title="The ID of the command to get")],
    pos: int = Query(default=0, ge=0, title="The position of the log to get"),
    size: int = Query(default=-1, title="The size of the log to get"),
):
    """get command log"""
    try:
        log = manager.get_script_log(tid, pos, size)
        print("response log", log.decode("gb2312", errors="ignore"))
        return Response(content=log, media_type="application/octet-stream")
    except ValueError as e:
        print("exception", e)
        return Response(content=str(e), status_code=400)


@router.get("/commands/tasks", summary="获取任务列表")
def get_tasks():
    """get task list"""
    task = {
        "lastUpdate": 0,
        "tasks": [
            {
                "taskId": t.taskid,
                "status": t.get_status(),
                "commandId": t.info.id,
                "createdAt": t.starttime,
                "cmdline": t.cmdline,
            }
            for _, t in manager.task.items()
        ],
    }

    for _, t in manager.task.items():
        if t.starttime and task["lastUpdate"] < t.starttime:
            task["lastUpdate"] = t.starttime

        if t.endtime and task["lastUpdate"] < t.endtime:
            task["lastUpdate"] = t.endtime

    if task["lastUpdate"] < manager.lastupdate:
        task["lastUpdate"] = manager.lastupdate

    print("task", task)
    return task


@router.delete("/commands/tasks/{tid}/delete", summary="删除任务")
def del_task(tid: Annotated[int, Path(title="The ID of the command to delete")]):
    """delete task"""
    print("delete task", tid)
    try:
        manager.del_task(tid)
        return {"code": 0, "message": "ok"}
    except ValueError as e:
        print("exception", e)
        return Response(
            content={"code": 400, "message": str(e)},
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )


@router.post("/commands/tasks/{tid}/stop", summary="停止任务")
def stop_task(tid: Annotated[int, Path(title="The ID of the command to stop")]):
    """stop running task"""
    print("stopping task", tid)
    try:
        manager.stop_task(tid)
        return {"code": 0, "message": "ok"}
    except ValueError as e:
        print("exception", e)
        return Response(
            content={"code": 400, "message": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json",
        )

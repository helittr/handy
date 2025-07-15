"""
ADB Script Manager API

Provides endpoints for managing and executing ADB commands through a RESTful API.
Includes WebSocket support for real-time task updates.
"""

import logging
from typing import Annotated
from fastapi import APIRouter, Path, Response, Query, status, WebSocket
from fastapi.responses import JSONResponse
from ..config.settings import SCRIPTS_JSON
from ..core.scriptManager import ScriptManager
from ..models.script import ExecuteParam, RootGroup, ManagerInfo
import asyncio

router = APIRouter(prefix="/adb", tags=["ADB"])

manager = ScriptManager(str(SCRIPTS_JSON))

def generate_task_list() -> dict:
    """Generate standardized task list structure"""
    task = {
        "lastUpdate": 0,
        "tasks": [
            {
                "taskId": t.taskid,
                "status": t.get_status().value if hasattr(t.get_status(), 'value') else t.get_status(),
                "commandId": t.info.id,
                "createdAt": t.starttime,
                "cmdline": t.cmdline,
                "logfile": str(t.logfile),
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

    logging.debug(f"Generated task list: {task}")
    return task

def handle_error_response(e: Exception, status_code: int = 400) -> JSONResponse:
    """Standard error response handler"""
    logging.error(f"API error: {str(e)}")
    return JSONResponse(
        content={"code": status_code, "status": "error", "message": str(e)},
        status_code=status_code,
    )


@router.get("/commands", summary="获取命令列表")
def get_commands():
    """
    获取所有可用的命令列表

    Returns:
        dict: 包含所有命令的分组结构
    """
    try:
        return manager.rootgroup
    except Exception as e:
        return handle_error_response(e)

@router.get("/commands/schema", summary="获取命令Schema")
def get_commands_schema():
    """
    获取所有命令的Schema定义

    Returns:
        dict: 包含所有命令的Schema信息
    """
    try:
        return RootGroup.model_json_schema()
    except Exception as e:
        return handle_error_response(e)

@router.post("/commands/reload", summary="重新加载命令")
def reload_commands():
    """
    重新加载命令列表

    Returns:
        dict: 包含重新加载状态的响应
    """
    try:
        manager.reload()
        return {"status": "ok", "code": 0, "message": "Commands reloaded successfully"}
    except Exception as e:
        return handle_error_response(e)

@router.post("/commands/{sid}/execute", summary="执行指定命令")
def exe_command(
    sid: Annotated[int, Path(title="命令ID", ge=1)],
    params: ExecuteParam,
):
    """
    执行指定的ADB命令
    
    Args:
        sid: 命令ID (必须大于0)
        params: 执行参数
        
    Returns:
        dict: 包含任务ID的成功响应或错误信息
    """
    logging.info(f"Executing command {sid} with params: {params}")
    try:
        tid = manager.execute_script(sid, params)
        return {"status": "ok", "code": 0, "data": {"taskId": tid}}
    except Exception as e:
        return handle_error_response(e)


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
        # logging.debug(f"response log: {log.decode('gb2312', errors='ignore')}")
        return Response(content=log, media_type="application/octet-stream")
    except ValueError as e:
        logging.error(f"exception: {e}")
        return Response(content=str(e), status_code=400)


@router.get("/commands/tasks", summary="获取任务列表")
def get_tasks():
    """
    获取当前所有任务的状态列表
    
    Returns:
        dict: 包含所有任务信息和最后更新时间
    """
    return generate_task_list()


@router.delete("/commands/tasks/{tid}/delete", summary="删除任务")
def del_task(tid: Annotated[int, Path(title="The ID of the command to delete")]):
    """delete task"""
    logging.info(f"delete task: {tid}")
    try:
        manager.del_task(tid)
        return {"code": 0, "message": "ok"}
    except ValueError as e:
        logging.error(f"exception: {e}")
        return JSONResponse(
            content={"code": 404, "message": str(e)},
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.post("/commands/tasks/{tid}/stop", summary="停止任务")
def stop_task(tid: Annotated[int, Path(title="The ID of the command to stop")]):
    """stop running task"""
    logging.info(f"stopping task: {tid}")
    try:
        manager.stop_task(tid)
        return {"code": 0, "message": "ok"}
    except ValueError as e:
        logging.info(f"exception: {e}")
        return JSONResponse(
            content={"code": 400, "message": str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

@router.websocket("/ws")
async def websocket_tasks(websocket: WebSocket):
    """
    WebSocket实时获取任务状态更新
    
    Parameters:
        websocket: WebSocket连接对象
        
    Behavior:
        - 每秒推送一次任务列表更新
        - 自动处理连接断开和错误
    """
    await websocket.accept()
    logging.info("WebSocket connection established")
    
    try:
        while True:
            try:
                # Send ping to check connection
                await websocket.send_text("ping")
                pong = await asyncio.wait_for(websocket.receive_text(), timeout=1)
                if pong != "pong":
                    raise ConnectionError("Invalid pong response")
                    break     
                    
                # Send task updates
                await websocket.send_json(generate_task_list())
                await asyncio.sleep(1)
            except asyncio.TimeoutError:
                logging.warning("WebSocket timeout, reconnecting...")
                await websocket.close()
                break
            except ConnectionError:
                logging.warning("WebSocket connection error, reconnecting...")
                await websocket.close()
                break
                
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
        logging.info("WebSocket connection closed")

@router.get('/info', summary='获取脚本管理器信息', response_model=ManagerInfo)
async def get_info():

    return ManagerInfo(logpath=str(manager.logdir.absolute()))

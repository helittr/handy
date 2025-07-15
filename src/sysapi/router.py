
import subprocess

from typing import Annotated
from fastapi import APIRouter, Body

router = APIRouter(prefix="/sys", tags=["SYS"])

@router.post('/start', summary='执行 shell 命令 start')
async def sys_start(path:Annotated[str,  Body()]):

    subprocess.run(['start', path], shell=True)
    return {"status": "ok", "code": 0}


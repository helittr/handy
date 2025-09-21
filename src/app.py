from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from utiles.env import is_nuitka

from adb import router as adb_router
from sysapi.router import router as sys_router
from settings import router as settings_router

app = FastAPI()

app.include_router(adb_router)
app.include_router(sys_router)
app.include_router(settings_router)

if is_nuitka():
    static_dir = Path(__file__).parent.joinpath("static")
else:
    static_dir = Path(__file__).parent.parent.joinpath("../handyUi/dist")

print(f"Static files directory: {static_dir}")
if static_dir.exists():
    app.mount('/static', StaticFiles(directory=static_dir), name="static")
else:
    print(f"Static files directory does not exist: {static_dir}")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/docs/")
def root():
    return RedirectResponse(url="/static/docs/index.html")
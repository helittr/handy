from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from adb.api.routes import router as adb_router

app = FastAPI()


app.include_router(adb_router)


static_dir = Path(__file__).parent.joinpath("static")
print(f"Static files directory: {static_dir}")
app.mount('/static', StaticFiles(directory=static_dir), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return RedirectResponse(url="static/index.html")

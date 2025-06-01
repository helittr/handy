from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .adb.api import router as adb_router

app = FastAPI()

app.include_router(adb_router)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello, World!"}


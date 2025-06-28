import uvicorn
from app import app
from threading import Thread
import webview
import logging


class UvicornThread(Thread):
    def run(self):
        config = uvicorn.Config(app, port=8001, log_level="info", reload=True)
        server = uvicorn.Server(config)
        server.run()


if __name__ == "__main__":
    uvicorn_thread = UvicornThread(daemon=True)
    uvicorn_thread.start()

    logging.info("Webview started and running.")

    mainwin = webview.create_window(
        "handy",
        "http://localhost:8001",
        width=1500,
        height=1000,
        draggable=True,
        resizable=True,
    )

    webview.start()

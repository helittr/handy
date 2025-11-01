import uvicorn
from .app import app
import logging
from  .utiles.env import is_nuitka


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    config = uvicorn.Config(app, port=8001, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()

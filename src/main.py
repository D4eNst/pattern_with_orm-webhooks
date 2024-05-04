import uvicorn
import logging

from fastapi import FastAPI

from data.config import settings
from api.routs import router as api_router
from bot import dp
from content.handlers.routs import main_router
from content.middlewares.middleware import rg_middlewares
from utils import app_start_with, app_stop_with

logging.basicConfig(level=logging.INFO)


def initialize_app() -> FastAPI:
    # register handlers and start/stop functions
    dp.include_router(main_router)
    rg_middlewares(dp)

    app = FastAPI(**settings.set_app_attributes)

    app.add_event_handler("startup", app_start_with)
    app.add_event_handler("shutdown", app_stop_with)
    app.include_router(router=api_router)

    return app


app = initialize_app()


if __name__ == "__main__":
    # To start, use the uvicorn command in terminal or in docker
    # If you want to launch the application using this entry point, make sure that the application
    # has access to the root of the project (for example, the path is set in PYTHONPATH)
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
        )
    except KeyboardInterrupt:
        pass

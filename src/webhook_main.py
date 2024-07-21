from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI

from api.routs import router as api_router
from bot import dp
from content.handlers.routs import main_router
from content.middlewares.middleware import register_middlewares
from data.config import settings
from logs import logging_config
from management import app_start_with, app_stop_with

dictConfig(logging_config)


def initialize_app() -> FastAPI:
    # register handlers and start/stop functions
    dp.include_router(main_router)
    register_middlewares(dp)

    tb_app = FastAPI(**settings.set_app_attributes)

    tb_app.add_event_handler("startup", app_start_with)
    tb_app.add_event_handler("shutdown", app_stop_with)
    tb_app.include_router(router=api_router)

    return tb_app


app = initialize_app()


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
        )
    except KeyboardInterrupt:
        pass

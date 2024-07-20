from aiogram import Router

from .basic.handlers import router as basic_router

main_router = Router()
main_router.include_routers(
    basic_router,
)

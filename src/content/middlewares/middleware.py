from aiogram import Dispatcher
from .db_session import DbSession


def rg_middlewares(dp: Dispatcher) -> None:
    # import and add your middlewares, for example:
    # dp.message.middleware.register(SomeMiddleware)
    dp.update.middleware.register(DbSession())

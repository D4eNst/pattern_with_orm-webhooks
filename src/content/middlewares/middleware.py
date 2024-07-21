from aiogram import Dispatcher
from .db_session import DbSession


def register_middlewares(dp: Dispatcher) -> None:
    # import and add your middlewares, for example:
    dp.update.middleware.register(DbSession())


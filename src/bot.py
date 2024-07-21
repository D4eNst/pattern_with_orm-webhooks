from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage

from data.config import settings
from repository.redis import redis_client

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

storage = RedisStorage(redis=redis_client)
dp = Dispatcher(storage=storage)

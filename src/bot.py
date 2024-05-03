from aiogram import Dispatcher, Bot
from repository.database import storage
from data.config import settings

bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

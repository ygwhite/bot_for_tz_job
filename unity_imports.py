from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

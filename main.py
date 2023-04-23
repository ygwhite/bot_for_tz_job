from aiogram.utils import executor
from aiogram import types
from unity_imports import dp
from handler import weather, exchange_rate, polls, random_picture


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Привет! Я могу показать тебе погоду в твоём городе, показать курс валют, прислать смешную картинку и создать опрос для группового чата")


exchange_rate.exchange_rate_start_handlers(dp)
weather.weather_start_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp)

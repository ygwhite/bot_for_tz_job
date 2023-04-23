import requests
import datetime
from config import open_weather_token
from aiogram import types, Dispatcher


# @dp.message_handler()
async def start_weather(message: types.Message):
    await message.reply(
        "Пришли погоду")


async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        print(data)
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Погода пока неясная)"
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"***Хорошего дня!***"
                            )

    except Exception:
        await message.reply("\U00002620 Проверьте название города \U00002620")


def weather_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_weather, commands=['weather'])
    dp.register_message_handler(get_weather)

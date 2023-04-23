import os
import random
from io import BytesIO
from icrawler.builtin import GoogleImageCrawler
import page as page
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from bs4 import BeautifulSoup

from unity_imports import bot, dp

animals_picture = GoogleImageCrawler(storage=)


r = requests.get('https://4tololo.ru/sites/default/files/images/20122112123618.jpg')
soup = BeautifulSoup(page.text, "html.parser")
allNews = soup.findAll('a', class_='lenta')



async def send_random_image(message: types.Message):
    response = requests.get('https://4tololo.ru/sites/default/files/images/20122112123618.jpg')
    image_content = BytesIO(response.content)
    await bot.send_photo(chat_id=message.chat.id, photo=image_content)


def weather_start_handlers(dp: Dispatcher):
    dp.register_message_handler(send_random_image, commands=['random_image'])
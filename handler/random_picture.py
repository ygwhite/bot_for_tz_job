import random
from io import BytesIO
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from bs4 import BeautifulSoup

from unity_imports import bot

animal_list = []
search_term = 'милые животные'

for page_num in range(1, 25):
    url = f'https://fonwall.ru/search?page={page_num}&q={search_term}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_tags = soup.find_all(class_='photo-item__img')
    for image_tag in image_tags:
        if 'src' in image_tag.attrs:
            img_url = image_tag['src']
            if img_url.startswith('//'):
                img_url = f'https:{img_url}'
        animal_list.append(image_tag['src'])


async def send_random_image(message: types.Message):
    image_content = BytesIO(response.content)
    random_animal = random.choice(animal_list)
    print(random_animal)
    await bot.send_photo(chat_id=message.chat.id, photo=random_animal)


def picture_start_handlers(dp: Dispatcher):
    dp.register_message_handler(send_random_image, commands=['random_image'])

from aiogram import types
from aiogram.types import Message

from unity_imports import dp

from aiogram.types import Poll, PollOption


async def create_poll(message: Message):
    # Здесь можно реализовать логику создания опроса
    poll = Poll(
        question='Какой ваш любимый цвет?',
        options=[
            PollOption('Синий', '1'),
            PollOption('Зеленый', '2'),
            PollOption('Красный', '3'),
            PollOption('Другой', '4')
        ]
    )
    await message.answer_poll(poll=poll)


async def send_polls(message: types.Message):
    dp.register_message_handler(create_poll, commands=['create_poll'])

import requests
import requests
import datetime
from aiogram.dispatcher import FSMContext
from config import open_weather_token
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

api_key = '2a0b3a1f1b4161039e582ac0'


class FSMrate(StatesGroup):
    first_сurrency = State()
    second_сurrency = State()
    amount = State()


async def first_rate(message: types.Message):
    await FSMrate.first_сurrency.set()
    print('1')
    await message.reply("Привет, введи первую валюту (Пример: RUB): ")


async def second_exchange_rate(message: types.Message, state: FSMContext):
    print('2')
    async with state.proxy() as data:
        data['first_сurrency'] = message.text
    await FSMrate.next()
    await message.reply("Теперь вторую: ")


async def amount_exchange_rate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_сurrency'] = message.text
        await FSMrate.next()
        await message.reply("А теперь сумму: ")


async def result_exchange_rate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = float(message.text)
    async with state.proxy() as data:
        for_first_сurrency = data.get('first_сurrency')
        for_second_сurrency = data.get('second_сurrency')
        for_amount = data.get('amount')
        response = requests.get(
            f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{for_first_сurrency}/{for_second_сurrency}/{for_amount}')
        conversion_result = response.json()
        await message.reply(f"Результат: {conversion_result.get('conversion_result')}")
        await state.finish()


def exchange_rate_start_handlers(dp: Dispatcher):
    dp.register_message_handler(first_rate, commands=['exchange_rate'], state=None)
    dp.register_message_handler(second_exchange_rate, content_types=['text'], state=FSMrate.first_сurrency)
    dp.register_message_handler(amount_exchange_rate, state=FSMrate.second_сurrency)
    dp.register_message_handler(result_exchange_rate, state=FSMrate.amount)

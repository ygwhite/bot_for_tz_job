# импортируем необходимые классы из библиотеки aiogram
from aiogram import Dispatcher, types
from aiogram.types import Poll, PollOption, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# создаем класс состояний и стейты
from unity_imports import dp, bot


class PollStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_options_count = State()
    waiting_for_option = State()

# функция-обработчик "запуска" опроса
async def start_poll_handler(message: types.Message, state: FSMContext):
    # запрос вопроса опроса
    await message.answer('Введите вопрос опроса:')
    # отправляем бота в состояние ожидания ввода вопроса
    await PollStates.waiting_for_question.set()

# функция-обработчик введенного вопроса
async def process_question_handler(message: types.Message, state: FSMContext):
    # сохраняем введенный вопрос и переходим в состояние ожидания количества ответов в опросе
    await state.update_data(question=message.text)
    await message.answer('Введите количество вариантов ответа:')
    await PollStates.waiting_for_options_count.set()

# функция-обработчик количества ответов в опросе
async def process_options_count_handler(message: types.Message, state: FSMContext):
    try:
        # пробуем получить введенное количество ответов и привести его к целому числу
        options_count = int(message.text)
    except ValueError:
        # если введеное пользователем не является числом, отправляем сообщение об ошибке
        await message.answer('Количество вариантов ответа должно быть числом. Попробуйте еще раз.')
        return

    # сохраняем количество ответов и переходим в состояние ожидания ввода самих вариантов ответа
    await state.update_data(options_count=options_count)
    await message.answer('Введите варианты ответа через запятую:')
    await PollStates.waiting_for_option.set()

# функция-обработчик введенных ответов
async def process_option_handler(message: types.Message, state: FSMContext):
    # преобразуем варианты ответа из строки в список
    options = message.text.split(',')

    # проверяем, что количество вариантов ответа равно тому, что мы ждали
    data = await state.get_data()
    if len(options) != data['options_count']:
        await message.answer(f'Вы ввели {len(options)}, а количество вариантов ответов должно быть {data["options_count"]}. Попробуйте еще раз.')
        return

    # создаем список объектов PollOption и создаем полный объект опроса
    poll_options = []
    for option in options:
        poll_options.append(PollOption(text=option.strip(), voter_count=0))

    poll = Poll(question=data['question'], options=poll_options, allows_multiple_answers=True, is_anonymous=False, type="quiz")

    # отправляем опрос
    await bot.send_poll(chat_id=message.chat.id, question=data['question'], options=poll_options)

    # завершаем работу с состояниями
    await state.finish()

def picture_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_poll_handler, commands=['start_poll'], state=None)
    dp.register_message_handler(process_question_handler, state=PollStates.waiting_for_question)
    dp.register_message_handler(process_options_count_handler, state=PollStates.waiting_for_options_count)
    dp.register_message_handler(process_option_handler, state=PollStates.waiting_for_option)
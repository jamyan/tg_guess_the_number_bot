from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import random
import os

bot = Bot(token=os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    maximum = State()
    random_number = State()
    number = State()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply('Hi! I am the Telegram bot. I can play Guess the number game. /start to start the game.')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await Form.random_number.set()
    await message.answer('I will guess the number from 1 to the number you choose.\nUpper limit:')

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok. The game was interrupted.\n/start to play again.')

@dp.message_handler(state=(Form.maximum, Form.random_number))
async def random_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['maximum'] = int(message.text)
        data['random_number'] = random.randint(1, data['maximum'])
    await Form.next()
    await message.reply('Ok. I am thinking of a number from 1 to {}. Try to guess it.'.format(data['maximum']))

@dp.message_handler(state=Form.number)
async def answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = int(message.text)
    if data['number'] == data['random_number']:
        await message.reply('Congratulations! You guessed!\n/start to play again')
        await state.finish()
    elif data['number'] > data['random_number']:
        await message.reply('Nope. The hidden number is less...')
        return answer
    elif data['number'] < data['random_number']:
        await message.reply('Nope. The hidden number is greater...')
        return answer

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import random

bot = Bot(token='TELEGRAM_API_TOKEN_HERE')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    number = State()

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.reply('Hi! I am the Telegram bot. I can play Guess the number game. /start to start the game')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await Form.number.set()
    global number
    number = random.randint(1, 100)
    await bot.send_message(message.chat.id, 'I thought of a number from 1 to 100. Try to guess it. (/cancel to stop the game)')

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok. The game was interrupted. /start to play again.')

@dp.message_handler(state=Form.number)
async def answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = int(message.text)
    if data['number'] == number:
        await message.reply('Congratulations! You guessed!')
        await state.finish()
    elif data['number'] > number:
        await message.reply('Nope. The hidden number is less...')
        return answer
    elif data['number'] < number:
        await message.reply('Nope. The hidden number is greater...')
        return answer

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

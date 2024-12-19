import asyncio
import logging
import aiogram

from aiogram import Bot, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from pip import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()




@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    print('Привет! Я бот помогающий твоему здоровью.')



async def start():
    await dp.start_polling(bot)

class UserState(StatesGroup):
    #(возраст, рост, вес)
    age = State()
    growth = State()
    weight = State()

@dp.message(Command('Calories'))
async  def set_age(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)

@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)

@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    norma = int(data['weight'])*10 + int(data['growth'])* 6.25 - int(data['age'])*5
    await message.answer(f'Ваша норма калорий в сутки; {norma}')
    await state.clear()

@dp.message()
async def cmd_not_start(message: Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print('exit')


#python module_13_4.py

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from misc import dp
from models import User
from keyboards import main_kb


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()

    if not User.get_or_none(user_id=message.from_user.id):
        await start_registration(message)
    else:
        await message.answer('🦋 Уже здоровались', reply_markup=main_kb)


@dp.message_handler(commands=['menu'], state='*')
async def menu(message: Message, state: FSMContext):
    await state.finish()

    if not User.get_or_none(user_id=message.from_user.id):
        await start_registration(message)
    else:
        await message.answer('🦋 Добро пожаловать в меню',
                             reply_markup=main_kb)


from .registration import start_registration

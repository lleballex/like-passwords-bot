from misc import dp
from models import User
from keyboards import main_kb
from states import Registration

from aiogram.types import Message
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'], state='*')
async def start(message: Message, state: FSMContext):
	await state.finish()

	if not User.get_or_none(user_id=message.from_user.id):
		await Registration.key_wait.set()
		await message.answer('Хаюшки! Придумай key')
	else:
		await message.answer('Уже здоровались', reply_markup=main_kb)


@dp.message_handler(commands=['menu'], state='*')
async def menu(message: Message, state: FSMContext):
	await state.finish()
	await message.answer('Добро пожаловать в меню', reply_markup=main_kb)


@dp.message_handler(state=Registration.key_wait)
async def save_key(message: Message, state: FSMContext):
	User.create(user_id=message.from_user.id, key=message.text)

	await message.delete()
	await message.answer('Ура! Теперь ты можешь добавить свой первый пароль. '
						 'Главное, не забывай свой key', reply_markup=main_kb)
	await state.finish()
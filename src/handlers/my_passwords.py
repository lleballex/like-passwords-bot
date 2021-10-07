from misc import dp
from states import MyPasswords
from misc import COMMANDS as CMDS
from models import User, Password
from keyboards import get_passwords_kb
from keyboards import inline_back_kb, password_kb

from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified


# do something if user does not exist
@dp.message_handler(lambda message: message.text == CMDS['my_passwords'])
async def my_passwords(message: Message):
	user = User.get(user_id=message.from_user.id)

	if user.passwords:
		await message.answer('Вот все твои пароли', reply_markup=get_passwords_kb(user))
	else:
		await message.answer('У тебя пока нет ни одного пароля')


@dp.callback_query_handler(lambda query: query.data.startswith('show_password:'), state='*')
async def show_password(query: CallbackQuery, state: FSMContext):
	await query.answer()
	await state.update_data(message=query.message,
							password_id=query.data.replace('show_password:', ''))
	await MyPasswords.key_wait.set()
	await query.message.edit_text('Для продолжения напиши свой key', reply_markup=inline_back_kb)


@dp.callback_query_handler(lambda query: query.data == 'show_passwords', state='*')
async def show_passwords(query: CallbackQuery, state: FSMContext):
	await query.answer()
	await state.finish()

	user = User.get(user_id=query.from_user.id)

	if user.passwords:
		await query.message.edit_text('Вот все твои пароли', reply_markup=get_passwords_kb(user))
	else:
		await query.message.edit_text('У тебя пока нет ни одного пароля')


@dp.message_handler(state=MyPasswords.key_wait)
async def check_key(message: Message, state: FSMContext):
	await message.delete()

	user = User.get(user_id=message.from_user.id)
	data = await state.get_data()

	if user.check_key(message.text):
		await state.finish()
		password = Password.get_or_none(id=data['password_id']).decipher(message.text)

		if password:
			await data['message'].edit_text(password.get_text_data(),
											reply_markup=password_kb,
											parse_mode=ParseMode.MARKDOWN_V2)
		else:
			await data['message'].edit_text('Пароля не существует. Наверное, он был удален')
	else:
		try:
			await data['message'].edit_text('Хм... Не подходит, попробуй еще раз',
											reply_markup=inline_back_kb)
		except MessageNotModified:
			pass


@dp.callback_query_handler(lambda query: query.data == 'hide_password', state='*')
async def hide_password(query: CallbackQuery):
	await query.answer()
	await query.message.delete()


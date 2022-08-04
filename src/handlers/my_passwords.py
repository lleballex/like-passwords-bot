from misc import dp
from states import MyPasswords
from misc import COMMANDS as CMDS
from models import User, Password
from keyboards import inline_back_kb, get_password_kb
from keyboards import get_passwords_kb, get_deletion_kb

from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified


# do something if user does not exist
@dp.message_handler(lambda message: message.text == CMDS['my_passwords'])
async def my_passwords(message: Message):
    user = User.get(user_id=message.from_user.id)

    if user.passwords:
        await message.answer('Вот все твои пароли',
                             reply_markup=get_passwords_kb(user))
    else:
        await message.answer('У тебя пока нет ни одного пароля')


@dp.callback_query_handler(lambda q: q.data.startswith('show_password:'),
                           state='*')
async def show_password(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.update_data(
        message=query.message,
        password_id=query.data.replace('show_password:', '')
    )
    await MyPasswords.key_wait.set()
    await query.message.edit_text('Для продолжения напиши свой ключ',
                                  reply_markup=inline_back_kb)


@dp.callback_query_handler(lambda q: q.data == 'show_passwords', state='*')
async def show_passwords(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.finish()

    user = User.get(user_id=query.from_user.id)

    if user.passwords:
        await query.message.edit_text('Вот все твои пароли',
                                      reply_markup=get_passwords_kb(user))
    else:
        await query.message.edit_text('У тебя пока нет ни одного пароля')


@dp.message_handler(state=MyPasswords.key_wait)
async def check_key(message: Message, state: FSMContext):
    await message.delete()

    user = User.get(user_id=message.from_user.id)
    data = await state.get_data()

    if user.check_key(message.text):
        await state.finish()
        password = Password.get_or_none(id=data['password_id'])

        if password:
            await data['message'].edit_text(
                password.decipher(message.text).get_text_data(),
                reply_markup=get_password_kb(password.id),
                parse_mode=ParseMode.MARKDOWN_V2)
        else:
            await data['message'].edit_text(
                'Пароля не существует. Наверное, он был удален')
    else:
        try:
            await data['message'].edit_text(
                'Хм... Не подходит, попробуй еще раз',
                reply_markup=inline_back_kb
            )
        except MessageNotModified:
            pass


@dp.callback_query_handler(lambda q: q.data == 'hide_password', state='*')
async def hide_password(query: CallbackQuery):
    await query.answer()
    await query.message.delete()


@dp.callback_query_handler(lambda q: q.data.startswith('delete_password:'),
                           state='*')
async def delete_password(query: CallbackQuery):
    await query.answer()
    id = int(query.data.replace('delete_password:', ''))
    await query.message.edit_text('Ты точно этого хочешь?',
                                  reply_markup=get_deletion_kb(id))


@dp.callback_query_handler(lambda q: q.data == 'cancel_deletion', state='*')
async def cancel_deletion(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text('Вот и хорошо')


@dp.callback_query_handler(lambda q: q.data.startswith('confirm_deletion:'),
                           state='*')
async def confirm_deletion(query: CallbackQuery):
    await query.answer()

    id = int(query.data.replace('confirm_deletion:', ''))
    Password.get(id=id).delete_instance()

    await query.message.edit_text('Так уж и быть, пароль удален')


@dp.callback_query_handler(lambda q: q.data.startswith('to_page:'), state='*')
async def change_passwords_page(query: CallbackQuery):
    await query.answer()

    user = User.get(user_id=query.from_user.id)
    page = int(query.data.replace('to_page:', ''))

    if user.passwords:
        await query.message.edit_text(
            'Вот все твои пароли', reply_markup=get_passwords_kb(user, page))
    else:
        await query.message.edit_text('У тебя пока нет ни одного пароля')

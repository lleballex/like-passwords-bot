from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ParseMode

from misc import dp
from states import MyPasswords
from misc import COMMANDS as CMDS
from models import User, Password
from keyboards import get_password_kb, to_passwords_kb
from keyboards import get_passwords_kb, get_password_deletion_kb
from .utils.key_management import clear_key, require_key, requiring_key_handler


def get_passwords_message(user_id: int, page=1):
    user = User.get(user_id=user_id)

    if user.passwords:
        return {
            'text': 'Вот все твои пароли',
            'reply_markup': get_passwords_kb(user, page),
        }
    else:
        return {
            'text': '🧐 У тебя пока нет ни одного пароля',
        }


async def send_password(message: Message, id: int, key: str):
    password = Password.get_or_none(id)

    if password:
        await message.edit_text(
            password.decipher(key).get_message(),
            reply_markup=get_password_kb(password.id),
            parse_mode=ParseMode.MARKDOWN_V2
        )
        return True
    else:
        await message.edit_text(
            '😬 Пароля не существует. Наверное, он был удален')
        return False


@dp.message_handler(lambda msg: msg.text == CMDS['my_passwords'])
async def my_passwords(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(**get_passwords_message(message.from_user.id))


@dp.callback_query_handler(lambda q: q.data.startswith('to_password:'),
                           state='*')
async def to_password(query: CallbackQuery, state: FSMContext):
    await query.answer()

    id = int(query.data.replace('to_password:', ''))
    key = await require_key(query.message, state, to_passwords_kb)

    if key:
        await send_password(query.message, id, key)
    else:
        await state.update_data(password_id=id)
        await MyPasswords.key.set()


@dp.callback_query_handler(lambda q: q.data == 'to_passwords', state='*')
async def to_passwords(query: CallbackQuery, state: FSMContext):
    await query.answer()

    if await state.get_state() == MyPasswords.key.state:
        await state.finish()
    else:
        await clear_key(state)

    await query.message.edit_text(**get_passwords_message(query.from_user.id))


@requiring_key_handler(MyPasswords.key)
async def to_password_after_key(message: Message, state: FSMContext, key: str):
    password_id = (await state.get_data())['password_id']
    await state.finish()
    return await send_password(message, password_id, key)


@dp.callback_query_handler(lambda q: q.data == 'hide_password', state='*')
async def hide_password(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await query.message.delete()
    await clear_key(state)


@dp.callback_query_handler(
    lambda q: q.data.startswith('to_password_deletion:'), state='*')
async def to_password_deletion(query: CallbackQuery):
    await query.answer()
    id = int(query.data.replace('to_password_deletion:', ''))
    await query.message.edit_text('Ты точно этого хочешь?',
                                  reply_markup=get_password_deletion_kb(id))


@dp.callback_query_handler(
    lambda q: q.data.startswith('delete_password:'), state='*')
async def delete_password(query: CallbackQuery):
    await query.answer()

    id = int(query.data.replace('delete_password:', ''))
    password = Password.get_or_none(id)

    if password:
        password.delete_instance()
        await query.message.edit_text('✅ Так уж и быть, пароль удален')
    else:
        await query.message.edit_text('😬 Кажется, пароль уже удален')


@dp.callback_query_handler(lambda q: q.data.startswith('to_passwords_page:'),
                           state='*')
async def change_passwords_page(query: CallbackQuery):
    await query.answer()
    page = int(query.data.replace('to_passwords_page:', ''))
    await query.message.edit_text(
        **get_passwords_message(query.from_user.id, page=page))

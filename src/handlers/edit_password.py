from misc import dp
from states import EditPassword
from misc import COMMANDS as CMDS
from models import Password, User
from keyboards import get_add_password_kb
from keyboards import main_kb, clear_field_kb

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove


async def send_fields(message: Message, state: FSMContext):
    data = await state.get_data()

    password: Password = data['password']
    fields = data.get('fields', {})

    await message.answer(
        'Что хочешь поменть?',
        reply_markup=get_add_password_kb(
            source=True,
            password=True,
            email=bool(fields.get('email', password.email)),
            phone=bool(fields.get('phone', password.phone)),
            username=bool(fields.get('username', password.username))),
    )
    await EditPassword.action.set()


async def update_field(message: Message, state: FSMContext, field: str):
    if message.text == CMDS['clear']:
        value = None
    else:
        value = message.text

    data = await state.get_data()
    fields = data.get('fields', {})
    fields[field] = value

    await state.update_data(fields=fields)
    await send_fields(message, state)


@dp.callback_query_handler(lambda q: q.data.startswith('edit_password:'),
                           state='*')
async def edit_password(query: CallbackQuery, state: FSMContext):
    id = int(query.data.replace('edit_password:', ''))
    password = Password.get(id)

    await state.update_data(password=password)
    await query.message.edit_text('Мне нужен твой ключ')
    await EditPassword.key.set()


@dp.message_handler(state=EditPassword.key)
async def check_key(message: Message, state: FSMContext):
    await message.delete()
    user: User = User.get(user_id=message.from_user.id)

    if user.check_key(message.text):
        await state.update_data(key=message.text)
        await send_fields(message, state) 
    else:
        await message.answer('😬 Не подходит, попробуй еще раз')


@dp.message_handler(lambda msg: msg.text == CMDS['back'],
                    state=EditPassword.action)
async def cancel_editing(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('😔 Значит в другой раз отредактируем',
                         reply_markup=main_kb)


@dp.message_handler(lambda msg: msg.text == CMDS['save'],
                    state=EditPassword.action)
async def finish_editing(message: Message, state: FSMContext):
    data = await state.get_data()

    password: Password = data['password']
    password.update_fields(data['key'], **data.get('fields', {}))

    await state.finish()
    await message.answer('✅ Супер! Данные изменены', reply_markup=main_kb)


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['source'],
                    state=EditPassword.action)
async def edit_source(message: Message):
    await message.answer('Напиши, откуда этот пароль',
                         reply_markup=ReplyKeyboardRemove())
    await EditPassword.source.set()


@dp.message_handler(state=EditPassword.source)
async def edit_source_process(message: Message, state: FSMContext):
    await update_field(message, state, 'source') 


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['email'],
                    state=EditPassword.action)
async def edit_email(message: Message):
    await message.answer('Напиши свою почту',
                         reply_markup=clear_field_kb)
    await EditPassword.email.set()


@dp.message_handler(state=EditPassword.email)
async def edit_email_process(message: Message, state: FSMContext):
    await update_field(message, state, 'email') 


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['username'],
                    state=EditPassword.action)
async def edit_username(message: Message):
    await message.answer('Какой у тебя логин?',
                         reply_markup=clear_field_kb)
    await EditPassword.username.set()


@dp.message_handler(state=EditPassword.username)
async def edit_username_process(message: Message, state: FSMContext):
    await update_field(message, state, 'username') 


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['phone'],
                    state=EditPassword.action)
async def edit_phone(message: Message):
    await message.answer('Давай свой номер телефона',
                         reply_markup=clear_field_kb)
    await EditPassword.phone.set()


@dp.message_handler(state=EditPassword.phone)
async def edit_phone_process(message: Message, state: FSMContext):
    await update_field(message, state, 'phone') 

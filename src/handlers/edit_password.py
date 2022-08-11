from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from misc import dp
from models import Password
from states import EditPassword
from misc import COMMANDS as CMDS
from keyboards import main_kb, clear_field_kb
from .utils.key_management import require_key, requiring_key_handler
from .utils.password_generator import send_generator, generator_handler
from keyboards import get_password_updating_kb, get_back_to_password_kb


async def send_fields(message: Message, state: FSMContext):
    data = await state.get_data()
    password: Password | None = Password.get_or_none(data['password_id'])

    if password:
        fields = data.get('fields', {})

        await message.answer(
            'Что хочешь поменть?',
            reply_markup=get_password_updating_kb(
                source=True,
                password=True,
                email=bool(fields.get('email', password.email)),
                phone=bool(fields.get('phone', password.phone)),
                username=bool(fields.get('username', password.username))),
            )
        await EditPassword.action.set()
    else:
        await state.finish()
        await message.answer('😬 Кажется, пароль уже удален',
                             reply_markup=main_kb)


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
    await query.answer()

    id = int(query.data.replace('edit_password:', ''))
    key = await require_key(query.message, state, get_back_to_password_kb(id))

    await state.update_data(password_id=id)

    if key:
        await query.message.delete()
        await send_fields(query.message, state)
    else:
        await EditPassword.key.set()


@requiring_key_handler(EditPassword.key)
async def edit_password_after_key(message: Message, state: FSMContext,
                                  _: str):
    await send_fields(message, state)
    return False


@dp.message_handler(lambda msg: msg.text == CMDS['back'],
                    state=EditPassword.action)
async def cancel_editing(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('😔 Значит, в другой раз отредактируем',
                         reply_markup=main_kb)


@dp.message_handler(lambda msg: msg.text == CMDS['save'],
                    state=EditPassword.action)
async def finish_editing(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()

    password = Password.get_or_none(data['password_id'])

    if password:
        password.update_fields(data['key'], **data.get('fields', {}))
        await message.answer('✅ Супер! Данные изменены', reply_markup=main_kb)
    else:
        await message.answer('😬 Кажется, этот пароль удален')


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['source'],
                    state=EditPassword.action)
async def edit_source(message: Message):
    await message.answer('Напиши, откуда этот пароль',
                         reply_markup=ReplyKeyboardRemove())
    await EditPassword.source.set()


@dp.message_handler(state=EditPassword.source)
async def edit_source_process(message: Message, state: FSMContext):
    await update_field(message, state, 'source') 


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['password'],
                    state=EditPassword.action)
async def edit_password_(message: Message):
    await message.answer('Какой у тебя парль?',
                         reply_markup=ReplyKeyboardRemove())
    await send_generator(message)
    await EditPassword.password.set()


@dp.message_handler(state=EditPassword.password)
async def edit_password__process(message: Message, state: FSMContext):
    await update_field(message, state, 'password')


@generator_handler(EditPassword)
async def generate_password_process(query: CallbackQuery, state: FSMContext,
                                    password: str):
    query.message.text = password
    await update_field(query.message, state, 'password')


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

from misc import dp
from .general import menu
from states import AddPassword
from misc import COMMANDS as CMDS
from models import User, Password
from keyboards import main_kb, back_kb
from keyboards import get_add_password_kb
from .utils.password_generator import send_generator, generator_handler

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery


async def get_kb(state):
    kwargs = {}
    data = await state.get_data()

    for i in data.keys():
        kwargs[i] = True
    kwargs.pop('key')

    return get_add_password_kb(**kwargs)


async def wait(message, state):
    await AddPassword.wait.set()
    await message.answer('Что будем делать дальше?',
                         reply_markup=await get_kb(state))


@dp.message_handler(lambda message: message.text == CMDS['add_password'])
async def add_password(message: Message):
    await AddPassword.key_wait.set()
    await message.answer('Для продолжения напиши свой ключ',
                         reply_markup=back_kb)


@dp.message_handler(lambda msg: msg.text == CMDS['back'], state=AddPassword)
async def go_to_menu(message: Message, state: FSMContext):
    await menu(message, state)


@dp.message_handler(lambda msg: msg.text == CMDS['save'], state=AddPassword)
async def save_password(message: Message, state: FSMContext):
    data = await state.get_data()

    if not data.get('source'):
        await AddPassword.source_wait.set()
        await message.answer('Нет-нет, сначала введи источник')
    elif not data.get('password'):
        await AddPassword.password_wait.set()
        await message.answer('Нет-нет, сначала введи пароль')
    else:
        user = User.get(user_id=message.from_user.id)
        Password.create(user=user, **data)

        await state.finish()
        await message.answer('Супер! Пароль сохранен', reply_markup=main_kb)


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['source'],
                    state=AddPassword)
async def set_source(message: Message, state: FSMContext):
    await AddPassword.source_wait.set()
    await message.answer('Напиши, откуда этот пароль (ВК, Инстаграм и т.д.)',
                         reply_markup=await get_kb(state))


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['password'],
                    state=AddPassword)
async def set_password(message: Message, state: FSMContext):
    await AddPassword.password_wait.set()
    await message.answer('Теперь напиши сам пароль',
                         reply_markup=await get_kb(state))
    await send_generator(message)


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['email'],
                    state=AddPassword)
async def set_email(message: Message, state: FSMContext):
    await AddPassword.email_wait.set()
    await message.answer('Я тебя слушаю')


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['username'],
                    state=AddPassword)
async def set_username(message: Message, state: FSMContext):
    await AddPassword.username_wait.set()
    await message.answer('Я тебя слушаю')


@dp.message_handler(lambda msg: msg.text[2:] == CMDS['phone'],
                    state=AddPassword)
async def set_phone(message: Message, state: FSMContext):
    await AddPassword.phone_wait.set()
    await message.answer('Я тебя слушаю')


# do something if user does not exist
@dp.message_handler(state=AddPassword.key_wait)
async def check_key(message: Message, state: FSMContext):
    await message.delete()
    user = User.get(user_id=message.from_user.id)

    if user.check_key(message.text):
        await state.update_data(key=message.text)
        await set_source(message, state)
    else:
        await message.answer('Хм... Не подходит, попробуй еще раз')


@dp.message_handler(state=AddPassword.source_wait)
async def source_process(message: Message, state: FSMContext):
    await state.update_data(source=message.text)

    if (await state.get_data()).get('password'):
        await wait(message, state)
    else:
        await set_password(message, state)


@dp.message_handler(state=AddPassword.password_wait)
async def password_process(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(password=message.text)
    await wait(message, state)


@dp.message_handler(state=AddPassword.email_wait)
async def email_process(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await wait(message, state)


@dp.message_handler(state=AddPassword.username_wait)
async def username_process(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await wait(message, state)


@dp.message_handler(state=AddPassword.phone_wait)
async def phone_process(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await wait(message, state)


@generator_handler(AddPassword)
async def generated_password_process(query: CallbackQuery, state: FSMContext,
                                     password: str):
    await state.update_data(password=password)
    await wait(query.message, state)

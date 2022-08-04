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
        await message.answer('Хаюшки! Придумай свою ключ. '
                             'Это может быть любое слово, '
                             'которое ты никогда не забудешь. Оно нужно, '
                             'чтобы обезопасить введеные тобой пароли, '
                             'без этого ключа их никто не узнает')
    else:
        await message.answer('Уже здоровались', reply_markup=main_kb)


@dp.message_handler(commands=['menu'], state='*')
async def menu(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Добро пожаловать в меню', reply_markup=main_kb)


@dp.message_handler(state=Registration.key_wait)
async def confirm_key(message: Message, state: FSMContext):
    await state.update_data(key=message.text)
    await message.delete()
    await Registration.key_confirmation_wait.set()
    await message.answer('А теперь отправь мне этот ключ еще раз')


@dp.message_handler(state=Registration.key_confirmation_wait)
async def save_key(message: Message, state: FSMContext):
    if (await state.get_data())['key'] == message.text:
        User.create(user_id=message.from_user.id, key=message.text)
        await message.answer('Ура! '
                             'Теперь ты можешь добавить свой первый пароль. '
                             'Главное, не забывай ключ',
                             reply_markup=main_kb)
        await state.finish()
    else:
        await state.reset_data()
        await Registration.key_wait.set()
        await message.answer('Хм, не сходится. '
                             'Давай начнем сначала, придумай свой ключ')

    await message.delete()

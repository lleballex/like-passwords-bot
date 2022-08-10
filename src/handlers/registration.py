from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from misc import dp
from models import User
from keyboards import main_kb
from states import Registration


async def start_registration(message: Message):
    await Registration.key.set()
    await message.answer('👋 Хаюшки! \n\nПридумай свою ключ. '
                         'Это может быть любое слово, не слишком большое, '
                         'которое ты никогда не забудешь. \n\nОно нужно, '
                         'чтобы обезопасить введеные тобой пароли - '
                         'без этого ключа их никто не узнает')


@dp.message_handler(state=Registration.key)
async def confirm_key(message: Message, state: FSMContext):
    await state.update_data(key=message.text)
    await message.delete()
    await Registration.key_confirmation.set()
    await message.answer('А теперь отправь мне этот ключ еще раз')


@dp.message_handler(state=Registration.key_confirmation)
async def save_key(message: Message, state: FSMContext):
    await message.delete()

    if (await state.get_data())['key'] == message.text:
        User.create(user_id=message.from_user.id, key=message.text)
        await state.finish()
        await message.answer('🎉 Ура! '
                             'Теперь ты можешь добавить свой первый пароль. '
                             'Главное, не забывай ключ',
                             reply_markup=main_kb)
    else:
        await state.finish()
        await Registration.key.set()
        await message.answer('😬 Хм, не сходится. '
                             'Давай начнем сначала, придумай свой ключ')

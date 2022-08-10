from typing import Callable, Awaitable

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.utils.exceptions import MessageNotModified

from misc import dp
from models import User
from keyboards import to_passwords_kb


async def clear_key(state: FSMContext):
    data = await state.get_data()
    data.pop('key', None)
    await state.set_data(data)


async def require_key(message: Message, state: FSMContext) -> str | None:
    key = (await state.get_data()).get('key')

    if key:
        return key
    else:
        await state.set_data({'message': message,})
        await message.edit_text('Для продолжения напиши свой ключ',
                                reply_markup=to_passwords_kb)


def requiring_key_handler(required_state: State):
    def decorator(callback: Callable[[Message, FSMContext, str],
                                     Awaitable[bool]]):
        @dp.message_handler(state=required_state)
        async def check_key(message: Message, state: FSMContext):
            await message.delete()

            user = User.get(user_id=message.from_user.id)
            data = await state.get_data()

            if user.check_key(message.text):
                if await callback(data['message'], state, message.text):
                    await state.finish()
                    await state.set_data({'key': message.text})
                else:
                    await state.finish()
            else:
                try:
                    await data['message'].edit_text(
                        '😬 Не подходит, попробуй еще раз',
                        reply_markup=to_passwords_kb
                    )
                except MessageNotModified:
                    pass

        return check_key
    return decorator

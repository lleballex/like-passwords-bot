from misc import dp
from keyboards import generate_password_kb, generated_password_kb

from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import escape_md
from aiogram.types import Message, CallbackQuery, ParseMode

import string
import random
from typing import Callable, Awaitable


ALPHABET = string.digits + string.ascii_lowercase + \
    string.ascii_uppercase + string.punctuation


async def send_generator(message: Message):
    await message.answer('Если хочешь, я могу его сгенерировать',
                         reply_markup=generate_password_kb)


def generator_handler(state):
    @dp.callback_query_handler(lambda q: q.data == 'hide_generated_password',
                               state='*')
    async def hide_generated_password(query: CallbackQuery):
        await query.answer()
        await query.message.delete()

    def decorator(callback: Callable[[CallbackQuery, FSMContext, str],
                                     Awaitable[None]]):
        @dp.callback_query_handler(lambda q: q.data == 'generate_password',
                                   state=state)
        async def generate_password(query: CallbackQuery, state: FSMContext):
            password = ''.join([random.choice(ALPHABET) for _ in range(13)])
            await query.message.edit_text(
                f'Вот пароль: `{escape_md(password)}`',
                reply_markup=generated_password_kb,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            await callback(query, state, password)

        return generate_password
    return decorator

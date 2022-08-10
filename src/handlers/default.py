from aiogram.types import Message

from misc import dp
from keyboards import main_kb


@dp.message_handler()
async def default_handler(message: Message):
    await message.answer('🧐 А правда, что слоны очень любят сыр?',
                         reply_markup=main_kb)

from peewee import SqliteDatabase
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import getenv


BOT_TOKEN = getenv('BOT_TOKEN')
assert BOT_TOKEN is not None

DATABASE = 'db.sqlite3'

ENCRYPTION_ALGORITHM = 'HS256'

COMMANDS = {
    'my_passwords': '🗂️ Мои пароли',
    'add_password': '🆕 Добавить пароль',
    'back': '⬅️ Назад',
    'save': '☑️ Сохранить',
    'hide': '👁️ Скрыть',
    'delete': '🗑 Удалить',
    'cancel_deletion': '😌 Нет, оставить',
    'confirm_deletion': '😱 Да, удалить',
    'source': 'Источник',
    'password': 'Пароль',
    'email': 'Email',
    'username': 'Логин',
    'phone': 'Телефон',
}


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SqliteDatabase(DATABASE)

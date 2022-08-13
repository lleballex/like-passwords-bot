from peewee import SqliteDatabase
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from os import getenv


BOT_TOKEN = getenv('BOT_TOKEN')
assert BOT_TOKEN is not None

USE_LONGPOLL = getenv('USE_LONGPOLL') == 'True'
WEBHOOK_HOST = getenv('WEBHOOK_HOST')
assert WEBHOOK_HOST is not None or USE_LONGPOLL
WEBHOOK_PATH = getenv('WEBHOOK_PATH', '')
WEBAPP_HOST = getenv('WEBAPP_HOST', 'localhost')
WEBAPP_PORT = getenv('WEBAPP_PORT', 8000)
SSL_CERTIFICATE = getenv('SSL_CERTIFICATE')

DATABASE = 'db.sqlite3'

ENCRYPTION_ALGORITHM = 'HS256'

COMMANDS = {
    'my_passwords': '🗂️ Мои пароли',
    'add_password': '🆕 Добавить пароль',
    'back': '⬅️ Назад',
    'save': '✅ Сохранить',
    'hide': '👁️ Скрыть',
    'edit': '✏️ Изменить',
    'delete': '🗑 Удалить',
    'cancel_deletion': '😌 Нет, оставить',
    'confirm_deletion': '😱 Да, удалить',
    'source': 'Источник',
    'password': 'Пароль',
    'email': 'Email',
    'username': 'Логин',
    'phone': 'Телефон',
    'clear': '🧹 Очистить',
}


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SqliteDatabase(DATABASE)

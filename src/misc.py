from peewee import SqliteDatabase
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = ''

DATABASE = ''

ENCRYPTION_ALGORITHM = ''

COMMANDS = {
	'my_passwords': '🗂️ Мои пароли',
	'add_password': '🆕 Добавить пароль',
	'back': '⬅️ Назад',
	'save': '☑️ Сохранить',
	'hide': '👁️ Скрыть',
	'source': 'Источник',
	'password': 'Пароль',
	'email': 'Email',
	'username': 'Логин',
	'phone': 'Телефон',
}


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SqliteDatabase(DATABASE)
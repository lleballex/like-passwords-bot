from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
	key_wait = State()


class MyPasswords(StatesGroup):
	key_wait = State()


class AddPassword(StatesGroup):
	key_wait = State()
	source_wait = State()
	password_wait = State()
	email_wait = State()
	username_wait = State()
	phone_wait = State()
	wait = State()
from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    key = State()
    key_confirmation = State()


class MyPasswords(StatesGroup):
    key = State()


class AddPassword(StatesGroup):
    key = State()
    source = State()
    password = State()
    email = State()
    username = State()
    phone = State()
    action = State()


class EditPassword(StatesGroup):
    key = State()
    action = State()
    source = State()
    password = State()
    email = State()
    username = State()
    phone = State()

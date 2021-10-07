from misc import COMMANDS as CMDS

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(CMDS['my_passwords'], CMDS['add_password'])


back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.row(CMDS['back'])


inline_back_kb = InlineKeyboardMarkup()
inline_back_kb.row(InlineKeyboardButton(CMDS['back'], callback_data='show_passwords'))


password_kb = InlineKeyboardMarkup()
password_kb.row(InlineKeyboardButton(CMDS['back'], callback_data='show_passwords'),
				InlineKeyboardButton(CMDS['hide'], callback_data='hide_password'))


generate_password_kb = InlineKeyboardMarkup()
generate_password_kb.add(InlineKeyboardButton('🎲 Сгенерировать', callback_data='generate_password'))

generated_password_kb = InlineKeyboardMarkup()
generated_password_kb.add(InlineKeyboardButton('🎲 Перегенерировать', callback_data='generate_password'),
						  InlineKeyboardButton(CMDS['hide'], callback_data='hide_password'))


def get_add_password_kb(source=False, password=False, email=False, username=False, phone=False):
	def text(key, is_entered):
		return f'✅ {CMDS[key]}' if is_entered else f'❌ {CMDS[key]}'

	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.row(text('source', source), text('password', password))
	keyboard.row(text('email', email), text('username', username), text('phone', phone))
	keyboard.row(CMDS['back'], CMDS['save'])

	return keyboard


def get_passwords_kb(user):
	keyboard = InlineKeyboardMarkup()
	for password in user.passwords:
		keyboard.row(InlineKeyboardButton(password.source,
										  callback_data=f'show_password:{password.id}'))
	return keyboard
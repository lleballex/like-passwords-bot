from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from misc import COMMANDS as CMDS


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row(CMDS['my_passwords'], CMDS['add_password'])


back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.row(CMDS['back'])


to_passwords_kb = InlineKeyboardMarkup()
to_passwords_kb.row(InlineKeyboardButton(
    CMDS['back'], callback_data='to_passwords'))


generate_password_kb = InlineKeyboardMarkup()
generate_password_kb.add(InlineKeyboardButton(
    '🎲 Сгенерировать', callback_data='generate_password'))


generated_password_kb = InlineKeyboardMarkup()
generated_password_kb.add(
    InlineKeyboardButton('🎲 Перегенерировать',
                         callback_data='generate_password'),
    InlineKeyboardButton(CMDS['hide'],
                         callback_data='hide_password')
)


clear_field_kb = ReplyKeyboardMarkup(resize_keyboard=True)
clear_field_kb.add(CMDS['clear'])


def get_password_updating_kb(source=False, password=False, email=False,
                             username=False, phone=False):
    def text(key, is_entered):
        return f'🟢 {CMDS[key]}' if is_entered else f'🔴 {CMDS[key]}'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(text('source', source), text('password', password))
    keyboard.row(text('email', email), text('username', username),
                 text('phone', phone))
    keyboard.row(CMDS['back'], CMDS['save'])

    return keyboard


def get_passwords_kb(user, page=1):
    per_page = 6
    keyboard = InlineKeyboardMarkup(row_width=2)

    for password in user.passwords[(page-1)*per_page:page*per_page]:
        keyboard.insert(InlineKeyboardButton(
            password.source, callback_data=f'to_password:{password.id}'))

    keyboard.row()
    if page != 1:
        keyboard.insert(InlineKeyboardButton(
            '⬅️', callback_data=f'to_ppasswords_page:{page - 1}'))
    if len(user.passwords) > page * per_page:
        keyboard.insert(InlineKeyboardButton(
            '➡️', callback_data=f'to_ppasswords_page:{page + 1}'))

    return keyboard


def get_password_kb(id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton(CMDS['delete'], 
                             callback_data=f'to_password_deletion:{id}'),
        InlineKeyboardButton(CMDS['hide'], callback_data='hide_password'),
        InlineKeyboardButton(CMDS['edit'],
                             callback_data=f'edit_password:{id}'),
    )
    keyboard.add(InlineKeyboardButton(CMDS['back'],
                                      callback_data='to_passwords'))
    return keyboard


def get_password_deletion_kb(id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(CMDS['cancel_deletion'],
                             callback_data=f'to_password:{id}'),
        InlineKeyboardButton(CMDS['confirm_deletion'],
                             callback_data=f'delete_password:{id}'),
    )
    return keyboard


def get_back_to_password_kb(id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(CMDS['back'],
                                      callback_data=f'to_password:{id}'))
    return keyboard

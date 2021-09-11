from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def adding_kb(package_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Добавить",switch_inline_query_current_chat=""))
    keyboard.add(InlineKeyboardButton("Закончить добавление",callback_data=f"end_adding_{package_id}"))
    return keyboard
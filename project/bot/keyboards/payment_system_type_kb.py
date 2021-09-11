from aiogram.types import ReplyKeyboardMarkup

system_type_kb = ReplyKeyboardMarkup(resize_keyboard=True)
system_type_kb.row("Payme","Click")
system_type_kb.add("Назад")
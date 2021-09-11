from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

settings_kb = ReplyKeyboardMarkup(resize_keyboard=True)
settings_kb.row("Назад")
settings_kb.row("Сменить Ф.И.О","Сменить номер")
settings_kb.row("Добавить локацию","Удалить локацию")
from aiogram.types import ReplyKeyboardMarkup

money_kb = ReplyKeyboardMarkup(resize_keyboard=True)
money_kb.row("Наличные","Карта")
money_kb.add("Назад")
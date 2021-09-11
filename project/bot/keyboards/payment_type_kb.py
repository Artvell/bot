from aiogram.types import ReplyKeyboardMarkup

payment_type_kb = ReplyKeyboardMarkup(resize_keyboard=True)
payment_type_kb.row("Через приложение","Через телеграм")
payment_type_kb.add("Назад")
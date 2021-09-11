from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import Category

category_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
category_keyboard.row(KeyboardButton("Назад"))
for category in Category.select():
    btn = KeyboardButton(category.category)
    category_keyboard.row(btn)

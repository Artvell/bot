from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import Category

category_kb = InlineKeyboardMarkup()
category_kb.row(InlineKeyboardButton("Назад",callback_data="back"))
for category in Category.select():
    btn = InlineKeyboardButton(category.category, callback_data=category.category)
    category_kb.add(btn)

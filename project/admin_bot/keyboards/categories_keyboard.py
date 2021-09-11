from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Category

category_kb = InlineKeyboardMarkup()
for category in Category.select():
    btn = InlineKeyboardButton(category.category,callback_data=f"category_{category.id}")
    category_kb.row(btn)
category_kb.row(InlineKeyboardButton("❌",callback_data="❌"))
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Subcategory, Category

def subcategories_kb(subcategories):
    subcategory_kb = InlineKeyboardMarkup()
    subcategory_kb.row(InlineKeyboardButton("Назад",callback_data="back"))
    for subcategory in subcategories:
        btn = InlineKeyboardButton(subcategory.subcategory, callback_data=subcategory.subcategory)
        subcategory_kb.add(btn)
    return subcategory_kb
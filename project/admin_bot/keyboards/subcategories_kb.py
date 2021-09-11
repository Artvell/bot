from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Subcategory, Category

def subcategories_kb(subcategories):
    subcategory_kb = InlineKeyboardMarkup()
    subcategory_kb.row(InlineKeyboardButton("Назад",callback_data="bact_to_categ"))
    for subcategory in subcategories:
        btn = InlineKeyboardButton(subcategory.subcategory,callback_data=f"subcateg_{subcategory.id}")
        subcategory_kb.row(btn)
    return subcategory_kb
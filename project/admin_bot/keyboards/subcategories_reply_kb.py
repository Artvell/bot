from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import Subcategory, Category

def subcategories_keyboard(subcategories):
    subcategory_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    subcategory_keyboard.row(KeyboardButton("Назад"))
    for subcategory in subcategories:
        btn = KeyboardButton(subcategory.subcategory)
        subcategory_keyboard.row(btn)
    return subcategory_keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

product_kb = InlineKeyboardMarkup()
prev_btn = InlineKeyboardButton("Предыдущий", callback_data="Предыдущий")
next_btn = InlineKeyboardButton("Следующий", callback_data="Следующий")
bascket = InlineKeyboardButton("Корзина", callback_data="Корзина")
product_kb.row(prev_btn,next_btn)
product_kb.row(bascket)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def numbers_kb(prod_id):
    keyboard = InlineKeyboardMarkup()
    for i in range(1,10):
        btn = InlineKeyboardButton(i,callback_data=f"product_{prod_id}_{i}")
        keyboard.insert(btn)
    keyboard.add(InlineKeyboardButton("❌",callback_data="❌"))
    return keyboard
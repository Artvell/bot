from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def menu_kb():
    keyboard = InlineKeyboardMarkup()
    #btn_1 = InlineKeyboardButton("Товары", callback_data="products")
    btn_2 = InlineKeyboardButton("Поиск",switch_inline_query_current_chat="")
    btn_3 = InlineKeyboardButton("Категории", callback_data="categories")
    btn_4 = InlineKeyboardButton("Корзина", callback_data="basket")
    #keyboard.add(btn_1)
    keyboard.add(btn_3)
    keyboard.add(btn_2)
    keyboard.add(btn_4)
    return keyboard
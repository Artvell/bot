from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def package_kb(package_id):
    package_keyboard = InlineKeyboardMarkup()
    add_product_btn = InlineKeyboardButton("Добавить продукт",callback_data=f"add_to_package_{package_id}")
    cost_btn = InlineKeyboardButton("Установить цену",callback_data=f"set_cost_package_{package_id}")
    delete_btn = InlineKeyboardButton("Удалить пакет",callback_data=f"delete_package_{package_id}")
    package_keyboard.row(add_product_btn,cost_btn).add(delete_btn)
    return package_keyboard
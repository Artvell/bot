from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def basket_kb(products):
    basket_keyboard = InlineKeyboardMarkup(row_width=2)
    for product in products:
        flag = 1 if product['is_package'] else 0
        btn = InlineKeyboardButton("❌"+product["name"],callback_data=f"delete_{product['id']}_{flag}")
        basket_keyboard.insert(btn)
    clear_btn = InlineKeyboardButton("Очистить корзину",callback_data="clear_basket")
    buy_btn = InlineKeyboardButton("Оформить заказ",callback_data="create_order")
    basket_keyboard.add(clear_btn)
    basket_keyboard.add(buy_btn)
    return basket_keyboard

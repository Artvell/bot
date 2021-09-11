from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def product_keyboard(flag=False,is_available=True,is_visible=True):
    product_kb = InlineKeyboardMarkup()
    prev_btn = InlineKeyboardButton("Предыдущий", callback_data="Предыдущий")
    next_btn = InlineKeyboardButton("Следующий", callback_data="Следующий")
    if not flag:
        category = InlineKeyboardButton("Привязать", callback_data="link")
    else:
        category = InlineKeyboardButton("Отвязать", callback_data="unlink")
    if is_available:
        availablity_btn = InlineKeyboardButton("Убрать из наличия", callback_data="invert_availabl")
    else:
        availablity_btn = InlineKeyboardButton("Добавить в наличие", callback_data="invert_availabl")
    if is_visible:
        visibility_btn = InlineKeyboardButton("✅ Отображается", callback_data="invert_visibility")
    else:
        visibility_btn = InlineKeyboardButton("❌ Не отображается", callback_data="invert_visibility")
    cost = InlineKeyboardButton("Установить цену",callback_data="set_cost")
    product_kb.row(prev_btn,next_btn)
    product_kb.row(category)
    product_kb.row(availablity_btn)
    product_kb.row(cost)
    product_kb.row(visibility_btn)
    return product_kb
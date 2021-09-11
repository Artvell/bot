from aiogram.types import ReplyKeyboardMarkup
from models import Order, User

def order_list_kb(status, user_id):
    if status == "Выполняются":
        orders = Order.select().join(User).where((Order.status == 2) & (User.user_id == user_id))
    elif status == "Предзаказ":
        orders = Order.select().join(User).where((Order.status == 1) & (User.user_id == user_id))
    elif status == "Закрытые":
        orders = Order.select().join(User).where((Order.status == 3) & (User.user_id == user_id))
    else:
        orders = Order.select().join(User).where((Order.status == 4) & (User.user_id == user_id))
    kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    kb.add("Назад")
    for order in orders:
        kb.insert(f"Заказ {order.id}")
    return kb
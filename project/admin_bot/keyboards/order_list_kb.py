from aiogram.types import ReplyKeyboardMarkup
from models import Order

def order_list_kb(status):
    if status == "Выполняются":
        orders = Order.select().where(Order.status == 2)
    elif status == "Предзаказ":
        orders = Order.select().where(Order.status == 1)
    elif status == "Закрытые":
        orders = Order.select().where(Order.status == 3)
    else:
        orders = Order.select().where(Order.status == 4)
    kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    kb.add("Назад")
    for order in orders:
        kb.insert(f"Заказ {order.id}")
    return kb
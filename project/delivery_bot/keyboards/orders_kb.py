from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import Order,Route
from geopy.distance import geodesic
from peewee import JOIN

def orders_kb():
    orders_keyboard = InlineKeyboardMarkup(row_width=1)
    orders = Order.select().join(Route,JOIN.LEFT_OUTER).where(
                (Order.status == 2) &
                (Order.order_type == 2) &
                (Order.payment_status != 0) &
                (Route.id.is_null())
            )
    for order in orders:
        distance = geodesic((41.297252,69.268511), (order.latitude, order.longitude)).km
        distance = round(distance,2)
        btn = InlineKeyboardButton(f"Заказ №{order.id} (~{distance} км)",callback_data=f"get_order_{order.id}")
        orders_keyboard.row(btn)
    return orders_keyboard
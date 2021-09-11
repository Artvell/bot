from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import base64

def order_kb(from_coords, to_coords, order_id):
    keyboard = InlineKeyboardMarkup()
    coords = f"{from_coords[0]}|{from_coords[1]}/{to_coords[0]}|{to_coords[1]}"
    code = base64.b64encode(coords.encode("UTF-8")).decode("UTF-8")
    url = f"http://192.168.100.13:5000/route/{code}/"
    route_btn = InlineKeyboardButton("Посмотреть маршрут",url=url)
    start_btn = InlineKeyboardButton("Взять заказ",callback_data=f"start_order_{order_id}")
    keyboard.add(route_btn)
    keyboard.add(start_btn)
    return keyboard

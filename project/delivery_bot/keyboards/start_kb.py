from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from functions import is_driver

def start_kb(uid):
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if not is_driver(uid):
        phone_number_button = KeyboardButton("Отправить свой номер",request_contact=True)
        start_keyboard.add(phone_number_button)
    else:
        start_keyboard.row("Заказы")
        start_keyboard.row("Взятые заказы")
        start_keyboard.row("Выполненные заказы")
    return start_keyboard

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from functions import is_user_exists

def start_kb(uid):
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    feed_btn = KeyboardButton("Текстовая лента")
    category_btn = KeyboardButton("Категории")
    if not is_user_exists(uid):
        phone_number_button = KeyboardButton("Отправить свой номер",request_contact=True)
        start_keyboard.add(phone_number_button)
        start_keyboard.add(feed_btn)
        start_keyboard.add(category_btn)
    else:
        start_keyboard.add("Меню")
        start_keyboard.row("Акции","Связь с нами")
        start_keyboard.row("Мои заказы","Настройки")
    return start_keyboard


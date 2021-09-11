from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from functions import is_user_exists

def start_kb():
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_keyboard.row("Поиск", "Рассылка")
    start_keyboard.row("Товары","Категории")
    start_keyboard.row("Заказы", "Пакеты")
    start_keyboard.row("Добавить водителя","Удалить водителя")
    start_keyboard.row("Синхронизировать")
    return start_keyboard


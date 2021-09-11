from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import User

def locations_kb(user_id, flag=False, flag_2=True):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if flag_2:
        user_locat_btn = KeyboardButton("Отправить текущую локацию",request_location=True)
        kb.add(user_locat_btn)
    if not flag:
        user = User.get(User.user_id==user_id)
        if user.locations is not None:
            for location in user.locations:
                kb.add(location["name"])
    kb.add("Назад")
    return kb
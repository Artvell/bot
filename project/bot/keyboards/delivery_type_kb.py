from aiogram.types import ReplyKeyboardMarkup
def delivery_type(flag=True):
    if flag:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("Самовывоз","Доставка")
        kb.add("Предзаказ")
        kb.add("Назад")
    else:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row("Самовывоз","Доставка")
        kb.add("Назад")
    return kb
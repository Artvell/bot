"файл с функцией is_driver"
from models import Driver

def is_driver(uid):
    "функция для определения существования водителя"
    driver = Driver.get_or_none(user_id=uid)
    if driver is None:
        return False
    return True
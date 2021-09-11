"файл с функцией is_user_exists"
from models import User

def is_user_exists(uid):
    "функция для определения существования юзера"
    user = User.get_or_none(user_id=uid)
    if user is None:
        return False
    return True
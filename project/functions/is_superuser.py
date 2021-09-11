"файл с функцией is_superuser"
from models import SuperUser

def is_superuser(uid):
    "функция для определения существования суперюзера"
    user = SuperUser.get_or_none(user_id=uid)
    if user is None:
        return False
    return True
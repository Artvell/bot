from peewee import *
from models.database import db

class BasketClearingStats(Model):
    """Модель таблицы BasketClearingStats"""
    user_id = IntegerField()
    counter = IntegerField(default=1)
    class Meta:
        database = db
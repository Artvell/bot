from peewee import *
from models.database import db

class BasketStats(Model):
    """Модель таблицы BasketStats"""
    product_name = CharField(default="")
    counter = IntegerField(default=1)
    type = BooleanField(default=True) #1-добавление 0 - удаление
    class Meta:
        database = db
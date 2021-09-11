from peewee import *
from models.database import db

class CategStats(Model):
    """Модель таблицы CategStats"""
    name = CharField(default="")
    counter = IntegerField(default=1)
    pagination_counter = IntegerField(default=1)
    class Meta:
        database = db
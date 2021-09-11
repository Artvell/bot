from peewee import *
from models.database import db

class SearchStats(Model):
    """Модель таблицы SearchStats"""
    query = CharField(default="")
    success = BooleanField()
    counter = IntegerField(default=1)
    class Meta:
        database = db
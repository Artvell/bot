from peewee import *
from models.database import db

class Category(Model):
    """Модель таблицы Category"""
    category = CharField()
    class Meta:
        database = db
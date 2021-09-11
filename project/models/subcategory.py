from peewee import *
from models.database import db
from models import Category

class Subcategory(Model):
    """Модель таблицы Subcategory"""
    category = ForeignKeyField(Category,related_name="sybсategories",on_delete='CASCADE')
    subcategory = CharField()
    class Meta:
        database = db
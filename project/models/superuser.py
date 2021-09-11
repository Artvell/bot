from peewee import *
from models.database import db
from flask_login import UserMixin

class SuperUser(Model, UserMixin):
    """Модель таблицы User"""
    user_id = IntegerField(unique=True)
    phone = CharField()
    username = CharField(null=True)
    full_name = CharField(null=True)
    icon = CharField(null=True)
    is_main_admin = BooleanField(default=False, null=True)
    class Meta:
        database = db
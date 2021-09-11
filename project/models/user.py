from peewee import *
from models.database import db
import uuid
from models.jsonfield import JSONField

class User(Model):
    """Модель таблицы User"""
    user_id = IntegerField(unique=True)
    uuid = UUIDField(default=uuid.uuid4)
    phone = CharField()
    username = CharField(null=True)
    full_name = CharField(null=True)
    locations = JSONField()
    class Meta:
        database = db
    
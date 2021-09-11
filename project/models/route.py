from peewee import *
from models.database import db
import uuid
from models.jsonfield import JSONField
from models import Order, Driver

class Route(Model):
    """Модель таблицы Route"""
    uuid = UUIDField(default=uuid.uuid4)
    order = ForeignKeyField(Order, null=True, on_delete="CASCADE")
    driver = ForeignKeyField(Driver, null=True, on_delete="SET NULL")
    from_location = JSONField()
    to_location = JSONField()
    now_location = JSONField()
    status = IntegerField() # 1 - выполняется, 2 - закрыт
    class Meta:
        database = db
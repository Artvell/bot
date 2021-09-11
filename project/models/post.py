from peewee import *
from models.database import db
from models.subcategory import Subcategory, Category
from models import JSONField

class Post(Model):
    instagram_id = BigIntegerField(default=0)
    #created_at = TimestampField()
    name = CharField()
    text = TextField()
    likes = IntegerField()
    comments = IntegerField()
    links = JSONField()
    telegraph = CharField()
    category = ForeignKeyField(Category, null=True, on_delete = "SET NULL")
    subcategory = ForeignKeyField(Subcategory, null=True, on_delete = "SET NULL")
    cost = FloatField(default=0.0)
    is_available = BooleanField(default=True)
    is_visible = BooleanField(default=True)
    class Meta:
        database = db
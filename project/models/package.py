from peewee import *
from models.database import db
import uuid
from models.jsonfield import JSONField

class Package(Model):
    title = CharField()
    cost = FloatField(default=0.0)
    class Meta:
        database = db
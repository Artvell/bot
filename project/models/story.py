from peewee import *
from models.database import db

class Story(Model):
    created_at = TimestampField()
    link = TextField()
    expiry_time = TimestampField()
    type = IntegerField()
    class Meta:
        database = db
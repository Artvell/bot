from peewee import *
from models.database import db


class UserGrowth(Model):
    date = DateField()
    counter = IntegerField(default=1)
    class Meta:
        database = db
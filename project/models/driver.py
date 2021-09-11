from peewee import *
from models.database import db
from models.jsonfield import JSONField
from random import choice
from string import ascii_uppercase,ascii_lowercase , digits

class Driver(Model):
    user_id = IntegerField(null=True)
    phone = CharField()
    password = CharField()

    def generate_pass():
        return ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(15))

    class Meta:
        database = db
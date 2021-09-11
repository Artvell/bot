from peewee import *
from models.database import db
import uuid
from models.jsonfield import JSONField
from models import Post, Package

class ProductsInPackage(Model):
    package = ForeignKeyField(Package,on_delete="CASCADE")
    product = ForeignKeyField(Post,on_delete="CASCADE")
    class Meta:
        database = db
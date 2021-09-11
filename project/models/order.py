from peewee import *
from models.database import db
from models.jsonfield import JSONField
from models.user import User

class Order(Model):
    user = ForeignKeyField(User)
    order_created = DateTimeField()
    order = JSONField()
    status = IntegerField() #1-предзаказ, 2-выполняется, 3-закрыт, 4-ожидает оплаты
    order_summ = FloatField()
    longitude = FloatField(null=True)
    latitude = FloatField(null=True)
    client_asked_time = CharField(null=True)
    order_closed = DateTimeField(null=True)
    order_type = IntegerField() #1-самовывоз,2-доставка,3-предзаказ
    payment_status = IntegerField(null=True) #0-не оплачен, 1-наличные, 2 - карта, 3 - через телеграм
    payment_dop_info = CharField(null=True) #click/payme
    class Meta:
        database = db
"Подключение к базе данных"
from peewee import *
from models import config
db = MySQLDatabase(
                config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
                )
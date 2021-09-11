import logging
from delivery_bot import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage

bot = Bot(token=config.TOKEN)
storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_bot_delivery')
dp = Dispatcher(bot,storage=storage)
logging.basicConfig(level=logging.INFO)

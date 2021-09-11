from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import start_kb
from models import Route, Driver
from functions import is_driver
from time import sleep
from datetime import datetime

@dp.message_handler(content_types = types.ContentType.LOCATION,state="*")
async def current_location(message: types.Message, state):
    if is_driver(message.from_user.id):
        await message.answer("Ок")
        await state.update_data(
            now_location = [message.location.latitude,message.location.longitude],
            updated_time = datetime.now()
        )
    else:
        await message.answer("Вы были удалены из базы водителей")


@dp.edited_message_handler(content_types = types.ContentType.LOCATION, state="*")
async def edited_location(message: types.Message, state):
    if is_driver(message.from_user.id):
        await state.update_data(
            now_location = [message.location.latitude,message.location.longitude],
            updated_time = datetime.now()
        )
        driver = Driver.get(Driver.user_id == message.from_user.id)
        query = Route.update(
            now_location=[message.location.latitude,message.location.longitude]
            ).where((Route.driver == driver.id) & (Route.status == 1))
        query.execute()

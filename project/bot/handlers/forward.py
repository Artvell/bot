from aiogram import types
from bot.bot_class import dp,bot
from bot.states import States
from aiogram.types import ChatType
from models import User
from aiogram.utils.exceptions import ChatNotFound

@dp.channel_post_handler(content_types = types.ContentType.ANY,state="*")
async def forwarding(message: types.Message):
    try:
        for user in User.select():
            await message.forward(user.user_id)
    except ChatNotFound:
        user.delete_instance()
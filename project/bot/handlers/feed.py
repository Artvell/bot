from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
from functions import create_media_list


@dp.message_handler(text="Текстовая лента", state=States.main_menu)
async def get_feed(message: types.Message):
    for media_list in create_media_list():
        await bot.send_media_group(message.from_user.id, media_list)
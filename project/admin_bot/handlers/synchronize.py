from aiogram import types
from admin_bot.bot_class import dp,bot
from admin_bot.states import States
from instaparser import Parser

@dp.message_handler(text="Синхронизировать", state=States.main_menu)
async def synchronize(message: types.Message):
    await message.answer("Синхронизация начата, ждите")
    parser = Parser("beauty_care.uz")
    new_posts = parser.get_feed()
    new_stories = parser.get_story()
    await message.answer(f"Синхронизировано.\nПостов:{new_posts} Историй:{new_stories}")
from aiogram import types
from models import User
from bot.bot_class import dp,bot
from bot.states import States
from bot.keyboards import settings_kb

@dp.message_handler(content_types=types.ContentTypes.TEXT,state=States.settings_delete_location)
async def delete_location(message: types.Message,state):
    user = User.get(User.user_id==message.from_user.id)
    user.locations = [location for location in user.locations if not location["name"] == message.text]
    user.save()
    await message.answer("Локация удалена",reply_markup=settings_kb)
    await States.settings.set()
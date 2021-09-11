from aiogram import types
from models import User
from bot.bot_class import dp,bot
from bot.states import States
from bot.keyboards import settings_kb

@dp.message_handler(content_types=types.ContentTypes.LOCATION,state=States.settings_add_location)
async def add_location(message: types.Message,state):
    await state.update_data(
        location={
            "longitude": message.location.longitude,
            "latitude": message.location.latitude
        }
    )
    await message.answer(
        "Введите название локации",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад")
        )
    await States.settings_set_location_name.set()

@dp.message_handler(lambda message: message.text!="Назад",state=States.settings_set_location_name)
async def set_location_name(message: types.Message,state):
    user_data = await state.get_data()
    user = User.get(User.user_id==message.from_user.id)
    if user.locations is None:
        user.locations = [
            {
                "name": message.text,
                "longitude": user_data["location"]["longitude"],
                "latitude": user_data["location"]["latitude"]
            }
        ]
        user.save()
    else:
        user.locations.append(
            {
                "name": message.text,
                "longitude": user_data["location"]["longitude"],
                "latitude": user_data["location"]["latitude"]
            }
        )
        user.save()
    await message.answer("Локация сохранена",reply_markup=settings_kb)
    await States.settings.set()
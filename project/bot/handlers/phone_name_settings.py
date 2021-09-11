from aiogram import types
from bot.bot_class import dp
from bot.states import States
from bot.keyboards import settings_kb, locations_kb
from models import User
import re

phone_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
phone_btn = types.KeyboardButton("Отправить номер", request_contact=True)
phone_kb.add("Назад").add(phone_btn)

@dp.message_handler(lambda message: message.text in ["Сменить Ф.И.О","Сменить номер","Добавить локацию","Удалить локацию"], state=States.settings)
async def change(message: types.Message):
    if message.text == "Сменить Ф.И.О":
        await States.settings_name.set()
        await message.answer("Введите ваши Ф.И.О",reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад"))
    elif message.text == "Сменить номер":
        await States.settings_phone.set()
        await message.answer("Введите или отправьте ваш номер в формате +998XXXXXXXXX",reply_markup=phone_kb)
    elif message.text == "Добавить локацию":
        await States.settings_add_location.set()
        await message.answer("Отправьте локацию",reply_markup=locations_kb(message.from_user.id, True))
    else:
        await States.settings_delete_location.set()
        await message.answer("Выберите локацию из списка",reply_markup=locations_kb(message.from_user.id,False,False))  

@dp.message_handler(content_types=[types.ContentType.TEXT,types.ContentType.CONTACT],state=States.settings_phone)
async def change_phone(message: types.Message):
    user = User.get(User.user_id==message.from_user.id)
    if "contact" in message:
        user.phone = message.contact.phone_number
        user.save()
        await States.settings.set()
        await message.answer("Номер изменен",reply_markup=settings_kb)
    else:
        if re.match(r"\+998\d{9}",message.text) is None:
            await message.answer("Неправильный формат")
        else:
            user.phone = message.text
            user.save()
            await States.settings.set()
            await message.answer("Номер изменен",reply_markup=settings_kb)


@dp.message_handler(content_types=types.ContentTypes.TEXT,state=States.settings_name)
async def change_name(message: types.Message):
    user = User.get(User.user_id==message.from_user.id)
    user.full_name = message.text
    user.save()
    await States.settings.set()
    await message.answer("ФИО изменены",reply_markup=settings_kb)
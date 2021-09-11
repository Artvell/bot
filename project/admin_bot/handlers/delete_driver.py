from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from admin_bot.keyboards import start_kb
from random import choice
from string import ascii_uppercase,ascii_lowercase , digits
from models import Driver
import re

@dp.message_handler(text="Удалить водителя", state=States.main_menu)
async def driver_phone_for_delete(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add("Назад")
    await message.answer("Отправьте номер телефона водителя",reply_markup=keyboard)
    await States.waiting_for_delete_driver.set()


@dp.message_handler(content_types=[
    types.ContentType.CONTACT,
    types.ContentType.TEXT
], state = States.waiting_for_delete_driver)
async def delete_driver(message: types.Message):
    if "contact" in message:
        number = message.contact.phone_number
        if number[0]!="+":
            number = "+" + number
    else:
        if re.match(r"\+998\d{9}",message.text) is None:
            await message.answer("Неправильный формат")
            number = None
        else:
            number = message.text
    if number is not None:
        driver = Driver.get_or_none(Driver.phone == number)
        if driver is not None:
            driver.delete_instance()
            await message.answer(
                "Водитель удален",
                reply_markup=start_kb()
            )
        else:
            await message.answer(
                "Водитель не найден",
                reply_markup=start_kb()
            )            
        await States.main_menu.set()
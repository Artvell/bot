from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from admin_bot.keyboards import start_kb

from models import Driver
import re

@dp.message_handler(text="Добавить водителя", state=States.main_menu)
async def driver_phone(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add("Назад")
    await message.answer("Отправьте номер телефона водителя",reply_markup=keyboard)
    await States.waiting_for_driver_phone.set()


@dp.message_handler(content_types=[
    types.ContentType.CONTACT,
    types.ContentType.TEXT
], state = States.waiting_for_driver_phone)
async def add_driver(message: types.Message):
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
        driver_pass = Driver.generate_pass()
        #driver_pass = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(15))
        Driver.create(
            phone = number,
            password = driver_pass
        )
        await message.answer(
            f"Пароль для водителя: {driver_pass}",
            reply_markup=start_kb()
        )
        await States.main_menu.set()
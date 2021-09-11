from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import start_kb
import re
from models import Driver

@dp.message_handler(content_types=[types.ContentType.CONTACT,types.ContentType.TEXT],state=States.waiting_for_phone)
async def get_phone(message: types.Message, state):
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
        if driver is None:
            await message.answer("Нет совпадений")
        else:
            await message.answer("Введите пароль")
            await state.update_data(driver_id=driver.id)
            await States.waiting_for_password.set()

@dp.message_handler(content_types=types.ContentTypes.TEXT,state=States.waiting_for_password)
async def get_password(message: types.Message, state):
    user_data = await state.get_data()
    driver_id = user_data["driver_id"]
    driver = Driver.get_by_id(driver_id)
    if message.text == driver.password:
        driver.user_id = message.from_user.id
        driver.save()
        await message.answer("Вы заригистрированы",reply_markup=start_kb(message.from_user.id))
        await state.reset_data()
        await States.main_menu.set()
    else:
        await message.answer("Неверный пароль")
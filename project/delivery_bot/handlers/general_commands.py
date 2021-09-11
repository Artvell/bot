from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import start_kb
from functions import is_driver


@dp.message_handler(commands=['start'], state = "*")
async def cmd_start(message: types.Message):
    if is_driver(message.from_user.id):
        await States.main_menu.set()
        await message.answer("Здравствуйте, водитель",reply_markup=start_kb(message.from_user.id))
    else:
        await message.answer("Вы не зарегистрированы! Пожалуйста, отправьте номер",reply_markup=start_kb(message.from_user.id))
        await States.waiting_for_phone.set()

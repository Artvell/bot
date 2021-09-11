from aiogram import types
from bot.bot_class import dp
from bot.states import States


@dp.message_handler(text="Связь с нами", state=States.main_menu)
async def info(message: types.Message):
    text="Здесь будут их контакты\nНу и инста: https://www.instagram.com/beauty_care.uz/"
    await message.answer(text)

@dp.message_handler(text="Акции", state=States.main_menu)
async def sales(message: types.Message):
    await message.answer("Тут пока ничего нет")
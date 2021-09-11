from aiogram import types
from bot.bot_class import dp
from bot.states import States
from bot.keyboards import settings_kb


@dp.message_handler(text="Настройки", state=States.main_menu)
async def settings(message: types.Message):
    await States.settings.set()
    await message.answer("Сменить настройки",reply_markup=settings_kb)
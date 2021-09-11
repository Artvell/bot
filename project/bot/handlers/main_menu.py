from aiogram import types
from bot.bot_class import dp
from bot.keyboards import menu_kb
from bot.states import States

@dp.message_handler(text="Меню",state="*")
async def main_menu(message: types.Message):
    await message.answer("⁣⁣⁣⁣⁣⁣⁣            Главное меню          ",reply_markup=menu_kb())
    await States.main_menu.set()
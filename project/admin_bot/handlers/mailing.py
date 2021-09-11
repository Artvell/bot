from aiogram import types
from aiogram.utils import exceptions
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from admin_bot.keyboards import start_kb
from bot.bot_class import bot as user_bot
from models import User

@dp.message_handler(text="Рассылка", state = States.main_menu)
async def get_message_text(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Назад")
    await message.answer("Отправьте то, что нужно разослать", reply_markup=keyboard)
    await States.waiting_for_spam.set()

@dp.message_handler(content_types=types.ContentType.ANY, state = States.waiting_for_spam)
async def send_message(message: types.Message):
    await message.forward(-1001444314123)
    await message.answer("Рассылается", reply_markup=start_kb())
    await States.main_menu.set()

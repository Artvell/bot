from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import orders_kb
from functions import is_driver

@dp.message_handler(text="Заказы",state=States.main_menu)
async def orders_list(message: types.Message):
    if is_driver(message.from_user.id):
        await message.answer("Текущие заказы", reply_markup=orders_kb())
    else:
        await message.answer("Вы были удалены из базы водителей")
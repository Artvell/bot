from aiogram import types
from bot.states import States
from bot.bot_class import dp,bot
from models import Order, Post, User
from functions import Formatter
from bot.keyboards import delivery_type


"""@dp.message_handler(content_types=types.ContentType.ANY,state="*")
async def eeeeee(message: types.Message):
    print("Куку")
    try:
        for user in User.select():
            await message.forward(user.user_id)
    except ChatNotFound:
        user.delete_instance()"""

@dp.callback_query_handler(lambda button: button.data.startswith("preorder_"), state="*")
async def accept_preorder(callback_query: types.CallbackQuery,state):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,"Выберите способ доставки",reply_markup=delivery_type(False))
    await state.update_data(
        order_flag = False,
        order_id = callback_query.data.split("_")[1]
    )
    await States.waiting_for_type.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from models import Order
from datetime import datetime

@dp.message_handler(lambda message: message.text.startswith("Закрыть заказ"), state=States.order_info)
async def close_order(message: types.Message):
    order_id = message.text.split()[-1]
    order = Order.get_or_none((Order.id == order_id) & (Order.status == 2))
    if order is not None:
        order.status = 3
        order.order_closed = datetime.now()
        order.save()
        await message.answer("Заказ закрыт")
    else:
        await message.answer(
            "Заказ уже закрыт или удален"
        )
from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import order_kb
from models import Order
from functions import is_driver

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("get_order_"),state="*")
async def order_info(callback_query: types.CallbackQuery, state):
    if is_driver(callback_query.from_user.id):
        user_data = await state.get_data()
        location = user_data.get("now_location", None)
        if location is not None:
            await callback_query.answer()
            order_id = callback_query.data.split("_")[-1]
            order = Order.get_by_id(order_id)
            text = "Заказ №{}\nОткрыт: {}\nВремя: {}\nЗаказчик: {}\nТелефон: {}"
            await bot.send_message(callback_query.from_user.id,text.format(
                    order.id,
                    order.order_created,
                    order.client_asked_time,
                    order.user.full_name,
                    order.user.phone
                    ),
                    reply_markup=order_kb(location,[order.latitude,order.longitude],order_id)
                )
        else:
            await callback_query.answer(
                "Для того чтобы брать заказы, нужно включить трансляцию местоположения!",
                show_alert=True
            )
    else:
        await callback_query.answer(
            "Вы были удалены из базы водителей",
            show_alert=True
        )

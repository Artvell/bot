from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from models import Route, Order
from datetime import datetime

@dp.callback_query_handler(lambda callback:callback.data.startswith("close_route_"), state = "*")
async def close_route(callback_query: types.CallbackQuery):
    route_id = callback_query.data.split("_")[-1]
    route = Route.get_or_none((Route.id == route_id) & (Route.status == 1))
    if route is None:
        await callback_query.answer("Этот маршрут уже закрыт или удален",show_alert=True)
    else:
        route.status = 2
        order = Order.get_by_id(route.order)
        order.order_closed = datetime.now()
        order.status = 3
        route.save()
        order.save()
        await bot.send_message(callback_query.from_user.id,"Заказ закрыт")

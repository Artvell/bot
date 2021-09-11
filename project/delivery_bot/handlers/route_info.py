from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from models import Route
from functions import is_driver

@dp.callback_query_handler(lambda callback:callback.data.startswith("route_"), state = "*")
async def route_info(callback_query: types.CallbackQuery):
    if is_driver(callback_query.from_user.id):
        route_id = callback_query.data.split("_")[1]
        route = Route.get_or_none(Route.id == route_id)
        if route is None:
            await callback_query.answer("Этот маршрут был удален")
        else:
            text = f"Маршрут № {route.id}.\nЗаказ № {route.order} \nВремя: {route.order.client_asked_time}"
            keyboard = types.InlineKeyboardMarkup()
            url = f"http://192.168.100.13:5000/map/{route.uuid}/"
            keyboard.add(types.InlineKeyboardButton("Маршрут", url=url))
            if route.status == 2:
                text += f"\nЗакрыт: {route.order.order_closed}"
            else:
                keyboard.add(types.InlineKeyboardButton("Заказ доставлен",callback_data=f"close_route_{route.id}"))
            await bot.send_message(
                callback_query.from_user.id,
                text,
                reply_markup=keyboard
            )
    else:
        await callback_query.answer(
            "Вы были удалены из базы водителей",
            show_alert=True
        )
    
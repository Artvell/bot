from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from delivery_bot.keyboards import order_kb
from bot.bot_class import bot as user_bot
from functions import is_driver
from models import Order, Route, Driver
from datetime import datetime

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("start_order_"),state="*")
async def create_route(callback_query: types.CallbackQuery,state):
    if is_driver(callback_query.from_user.id):
        order_id = callback_query.data.split("_")[-1]
        routes = Route.get_or_none(Route.order == order_id)
        if routes is not None:
            await callback_query.answer("Этот заказ уже взят другим курьером.",show_alert=True)
            await bot.delete_message(
                callback_query.from_user.id,
                callback_query.message.message_id
            )
        else:
            user_data = await state.get_data()
            now = datetime.now()
            last_updated = user_data.get("updated_time",None)
            diff = last_updated - now if last_updated is not None else None
            if last_updated is not None:
                diff = last_updated - now
                diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
                if diff_minutes > 5:
                    await callback_query.answer(
                        "Ваша геопозиция не транслируется!Для выполнения заказа, включите трансляцию местоположения",
                        show_alert=True
                    )
                else:
                    await callback_query.answer()
                    order = Order.get_by_id(order_id)
                    route = Route.create(
                        order = order,
                        driver = Driver.get(Driver.user_id == callback_query.from_user.id),
                        from_location = user_data["now_location"],
                        to_location = [order.latitude,order.longitude],
                        now_location = user_data["now_location"],
                        status = 1
                    )
                    text = f"Маршрут № {route.id}.\nЗаказ № {route.order} \nВремя: {route.order.client_asked_time}"
                    keyboard = types.InlineKeyboardMarkup()
                    url = f"http://192.168.100.13:5000/map/{route.uuid}/"
                    keyboard.add(types.InlineKeyboardButton("Маршрут", url=url))
                    keyboard.add(types.InlineKeyboardButton("Заказ доставлен",callback_data=f"close_route_{route.id}"))
                    await bot.send_message(
                        callback_query.from_user.id,
                        text,
                        reply_markup=keyboard
                    )
                    user_text = f"Курьер с вашим заказом № {route.order} выехал\n Его номер: {route.driver.phone}"
                    await user_bot.send_message(route.order.user.user_id, user_text)
            else:
                await callback_query.answer(
                    "Ваша геопозиция не транслируется!Для выполнения заказа, включите трансляцию местоположения",
                    show_alert=True
                )
    else:
        await callback_query.answer(
            "Вы были удалены из базы водителей",
            show_alert=True
        )
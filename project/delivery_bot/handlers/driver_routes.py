from aiogram import types
from delivery_bot.bot_class import dp,bot
from delivery_bot.states import States
from models import Driver, Route
from functions import is_driver

@dp.message_handler(text="Взятые заказы", state = States.main_menu)
async def opened_routes(message: types.Message, state):
    if is_driver(message.from_user.id):
        driver = Driver.get(Driver.user_id == message.from_user.id)
        routes = Route.select().where(
            (Route.driver == driver.id) &
            (Route.status == 1)
        )
        if routes.count() > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for route in routes:
                btn = types.InlineKeyboardButton(f"Заказ №{route.order}",callback_data=f"route_{route.id}")
                keyboard.row(btn)
            await message.answer("Ваши заказы: ", reply_markup=keyboard)
        else:
            await message.answer("У вас нет активных заказов")
    else:
        await message.answer("Вы были удалены из базы водителей")


@dp.message_handler(text="Выполненные заказы", state = States.main_menu)
async def closed_routes(message: types.Message, state):
    if is_driver(message.from_user.id):
        driver = Driver.get(Driver.user_id == message.from_user.id)
        routes = Route.select().where(
            (Route.driver == driver.id) &
            (Route.status == 2)
        )
        if routes.count() > 0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for route in routes:
                btn = types.InlineKeyboardButton(f"Заказ №{route.order}",callback_data=f"route_{route.id}")
                keyboard.row(btn)
            await message.answer("Закрытые заказы: ", reply_markup=keyboard)
        else:
            await message.answer("У вас нет закрытых заказов")
    else:
        await message.answer("Вы были удалены из базы водителей")
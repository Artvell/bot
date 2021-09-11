from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from functions import create_order_list
from admin_bot.keyboards import order_list_kb
from models import Order, Post
from functions import Formatter
import emoji


@dp.message_handler(text="Послать ссылку",state = States.order_info)
async def send_payment_link(message: types.Message, state):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Отмена",callback_data="canceling"))
    await message.answer("Отправьте ссылку для платежа",reply_markup=keyboard)
    await States.waiting_for_link.set()
    current_state = await state.get_state()
    user_data = await state.get_data()
    order = Order.get_by_id(user_data["order_id"])
    await state.update_data(
        payment_user_id = order.user.user_id,
        prev_state = current_state
    )

@dp.message_handler(text="Деньги получены",state = States.order_info)
async def order_paid(message: types.Message, state):
    user_data = await state.get_data()
    order = Order.get_by_id(user_data["order_id"])
    order.status = 2
    order.save()
    await message.answer("Заказ переведен в категорию <b>Выполняются</b>", parse_mode="HTML")

@dp.message_handler(text="Закрыть заказ",state = States.order_info)
async def order_paid(message: types.Message):
    user_data = await state.get_data()
    order = Order.get_by_id(user_data["order_id"])
    order.status = 3
    order.save()
    await message.answer("Заказ переведен в категорию <b>Закрытые</b>", parse_mode="HTML")
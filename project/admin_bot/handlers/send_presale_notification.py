from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from bot.bot_class import bot as user_bot
from models import Order, Post
from functions import Formatter

@dp.message_handler(text="Послать уведомление", state=States.order_info)
async def send_notification(message: types.Message, state):
    user_data = await state.get_data()
    order_id = user_data["order_id"]
    order = Order.get_by_id(order_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Оформить заказ", callback_data=f"preorder_{order_id}"))
    text = f"""Заказ №{order.id} <b>появился в наличии</b>
    Открыт: {order.order_created}
    Общая сумма заказа: {order.order_summ} сум

    <b>Подробнее о заказе:</b>\n"""
    for element in order.order:
        product = Post.get(Post.id == element["id"])
        name = f'<a href="{product.telegraph}">{Formatter(product).get_name()}</a>'
        text+=f"{name} {element['kol']} {int(element['kol'])*product.cost} сумов\n"
    
    await user_bot.send_message(
        Order.user.user_id,
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=keyboard
        )
    await message.answer("Уведомление отправлено пользователю")


@dp.callback_query_handler(lambda callback: callback.data.startswith("preorder_"),state="*")
async def send_preorder_info(callback_query: types.CallbackQuery):
    user_id, order_id, status = callback_query.data.split("_")[1:]
    await callback_query.answer()
    if status == "yes":
        order = Order.get_by_id(order_id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Оформить заказ", callback_data=f"preorder_{order_id}"))
        text = f"""Заказ №{order.id} <b>появился в наличии</b>
        Открыт: {order.order_created}
        Общая сумма заказа: {order.order_summ} сум

        <b>Подробнее о заказе:</b>\n"""
        for element in order.order:
            product = Post.get(Post.id == element["id"])
            name = f'<a href="{product.telegraph}">{Formatter(product).get_name()}</a>'
            text+=f"{name} {element['kol']} {int(element['kol'])*product.cost} сумов\n"
        
        await user_bot.send_message(
            user_id,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=keyboard
        )
    else:
        text = f"Заказа №{order_id} <b>пока нет в наличии</b>"
        await user_bot.send_message(
            user_id,
            text,
            parse_mode="HTML",
        )
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
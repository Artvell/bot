from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from bot.bot_class import bot as user_bot
from models import Order

@dp.callback_query_handler(lambda query: query.data.startswith("payment_"),state="*")
async def link_to_payment(callback_query: types.CallbackQuery,state):
    user_id, order_id = callback_query.data.split("_")[1:]
    order = Order.get_or_none(Order.id == order_id)
    if order is None or order.payment_status == 1 or order.payment_status == 2:
        await callback_query.answer("Заказ с таким номером уже оплачен или закрыт",show_alert=True)
    else:
        await callback_query.answer()
        current_state = await state.get_state()
        await state.update_data(
            payment_user_id = user_id,
            order_id = order_id,
            prev_state = current_state
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Отмена",callback_data="canceling"))
        await bot.send_message(callback_query.from_user.id,"Отправьте ссылку для платежа",reply_markup=keyboard)
        await States.waiting_for_link.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=States.waiting_for_link)
async def send_link(message: types.Message, state):
    user_data = await state.get_data()
    text = f"Пожалуйста, оплатите ваш заказ №{user_data['order_id']}\n{message.text}"
    await user_bot.send_message(user_data["payment_user_id"],text)
    await state.set_state(user_data["prev_state"])
    order = Order.get_by_id(user_data["order_id"])
    order.status = 4
    order.save()
    await state.set_state(user_data["prev_state"])
    await message.answer("Ссылка отправлена")

@dp.callback_query_handler(text="canceling", state=States.waiting_for_link)
async def cancel(callback_query: types.CallbackQuery, state):
    user_data = await state.get_data()
    await state.set_state(user_data["prev_state"])
    await callback_query.answer("Отменено!",show_alert=True)
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
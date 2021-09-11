from aiogram import types
from bot.bot_class import dp, bot
from admin_bot.bot_class import bot as admin
from bot.states import States
from bot.keyboards import order_list_kb
from models import Order, SuperUser

@dp.message_handler(text="Запросить ссылку для оплаты", state=States.order_info)
async def ask_link(message: types.Message, state):
    user_data = await state.get_data()
    order_id = user_data["order_id"]
    order = Order.get_by_id(order_id)
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Отправить ссылку для оплаты",callback_data=f"payment_{message.from_user.id}_{order.id}")
    keyboard.row(btn)
    text = f"Заказ № {order.id}.\nПользователь хочет оплатить его через {user_data['system']}. Пожалуйста, нажмите на кнопку и отправьте ссылку для оплаты\nСумма заказа: {order.order_summ}"
    await message.answer("Ссылка запрошена, скоро вы ее получите")
    for superuser in SuperUser.select():
        await admin.send_message(superuser.user_id,text,reply_markup=keyboard)

@dp.message_handler(text="Уточнить наличие", state=States.order_info)
async def ask_availability(message: types.Message, state):
    user_data = await state.get_data()
    order_id = user_data["order_id"]
    order = Order.get_by_id(order_id)
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Да",callback_data=f"preorder_{message.from_user.id}_{order_id}_yes")
    btn_2 = types.InlineKeyboardButton("❌ Нет",callback_data=f"preorder_{message.from_user.id}_{order_id}_no")
    keyboard.row(btn, btn_2)
    text = f"Предзаказ № {order.id}.\nПользователь спрашивает появился ли он в наличии?"
    await message.answer("Скоро вам ответят.")
    for superuser in SuperUser.select():
        await admin.send_message(superuser.user_id,text,reply_markup=keyboard)
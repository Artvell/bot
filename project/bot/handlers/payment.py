from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
import bot.keyboards as kb
from functions import create_order_list

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.select_system_type)
async def get_system_type(message: types.Message,state):
    systems = ["Click","Payme"]
    if message.text in systems:
        await state.update_data(system=message.text)
        await States.select_payment_type.set()
        await message.answer("Выберите способ оплаты",reply_markup=kb.payment_type_kb)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=States.select_payment_type)
async def get_system_type(message: types.Message,state):
    if (message.text == "Через приложение" or message.text == "Через телеграм") and message.text!="Назад":
        user_data = await state.get_data()
        await state.update_data(payment_type=message.text)
        text = "Ваш заказ:\n"
        order_data = create_order_list(user_data["basket"])
        for data in order_data:
            text+=f"{data['name']} {data['ammount']} cум\n"
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row("Подтвердить","Отменить")
        await message.answer(text,reply_markup=kb)
        await States.waiting_for_approve.set()
from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
import admin_bot.keyboards as kb

@dp.message_handler(text="Назад", state="*")
async def back(message: types.Message,state):
    current_state = await state.get_state()
    to_main = [
        States.waiting_for_subcategory.state,
        States.waiting_for_order_type.state,
        States.waiting_for_driver_phone.state,
        States.waiting_for_spam.state,
        States.waiting_for_package_title.state
    ]
    if current_state in to_main:
        await States.main_menu.set()
        await message.answer("Главное меню",reply_markup=kb.start_kb())

    elif current_state == States.subcategories.state:
        await States.previous()
        await message.answer("Категории", reply_markup=kb.category_keyboard)

    elif current_state == States.orders_list.state:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Назад")
        keyboard.row("Ожидают оплаты","Выполняются")
        keyboard.row("Предзаказ", "Закрытые")
        await message.answer(
            "Выберите тип заказа",
            reply_markup=keyboard
            )
        await States.waiting_for_order_type.set()

    elif current_state == States.order_info.state:
        user_data = await state.get_data()
        await message.answer("Выберите заказ из списка",reply_markup=kb.order_list_kb(user_data["order_type"]))
        await States.orders_list.set()
from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
import bot.keyboards as kb
from bot.handlers import basket, create_order

@dp.message_handler(text="Назад", state="*")
async def back(message: types.Message,state):
    current_state = await state.get_state()
    to_main = [
        States.settings.state,
        States.waiting_for_subcategory.state,
        States.waiting_for_order_type.state
    ]
    to_settings = [
        States.settings_phone.state,
        States.settings_name.state,
        States.settings_add_location.state,
        States.settings_delete_location.state
    ]
    if current_state in to_main:
        await States.main_menu.set()
        await message.answer("Главное меню",reply_markup=kb.start_kb(message.from_user.id))
    elif current_state == States.subcategories.state:
        await States.previous()
        await message.answer("Категории", reply_markup=kb.category_kb)
    elif current_state in to_settings:
        await States.settings.set()
        await message.answer("Настройки",reply_markup=kb.settings_kb)
    elif current_state == States.settings_set_location_name.state:
        await States.settings_add_location.set()
        await message.answer("Отправьте локацию",reply_markup=kb.locations_kb(message.from_user.id,True))


    elif current_state == States.waiting_for_type.state:
        await States.main_menu.set()
        await message.answer("Корзина",reply_markup=kb.start_kb(message.from_user.id))
        await basket.basket(chat_id=message.from_user.id,state=state)
    elif current_state == States.waiting_for_time.state:
        user_data = await state.get_data()
        flag = user_data.get("order_flag",True)
        await States.waiting_for_type.set()
        await bot.send_message(message.from_user.id,"Выберите способ доставки",reply_markup=kb.delivery_type(flag))
    elif current_state == States.waiting_for_location.state:
        await States.waiting_for_time.set()
        await message.answer("Какое время вам удобно? Нажмите или введите",reply_markup=kb.time_kb)
    elif current_state == States.waiting_for_money_type.state:
        user_data = await state.get_data()
        if user_data["delivery_type"] == 1:
            await States.waiting_for_time.set()
            await message.answer("Какое время вам удобно? Нажмите или введите",reply_markup=kb.time_kb)
        elif user_data["delivery_type"] == 2:
            await States.waiting_for_location.set()
            await message.answer("Отправьте локацию или выберите из списка",reply_markup=kb.locations_kb(message.from_user.id))
            await state.update_data(location={})
    elif current_state == States.select_system_type.state:
        await States.waiting_for_money_type.set()
        await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)
    elif current_state == States.select_payment_type.state:
        await States.select_system_type.set()
        await message.answer("Выберите платежную систему",reply_markup=kb.system_type_kb)
    elif current_state == States.create_order.state:
        user_data = await state.get_data()
        if user_data["delivery_type"] == 1:
            await States.waiting_for_money_type.set()
            await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)
        elif user_data["delivery_type"] == 2:
            await States.select_payment_type.set()
            await message.answer("Выберите способ оплаты",reply_markup=kb.payment_type_kb)
    
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
        await message.answer("Выберите заказ из списка",reply_markup=kb.order_list_kb(user_data["order_type"],message.from_user.id))
        await States.orders_list.set()

        
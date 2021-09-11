from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
import bot.keyboards as kb
from models import User, Order,Post, Package
from functions import create_order_list, best_product_id, create_product_message
import re
import datetime

@dp.callback_query_handler(text="create_order", state=States.main_menu)
async def select_type(callback_query: types.CallbackQuery,state):
    await callback_query.answer()
    best_id = best_product_id()
    await state.update_data(selected_id=best_id)
    product,caption,prod_id = create_product_message(best_id)
    await bot.send_photo(
        callback_query.from_user.id,
        product,
        "<b>Самое популярное</b>"+caption,
        reply_markup=kb.product_kb,
        parse_mode="HTML"
    )
    await bot.send_message(callback_query.from_user.id,"Выберите способ доставки",reply_markup=kb.delivery_type())
    await States.waiting_for_type.set()
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.message_handler(lambda message:message.text in ["Самовывоз","Доставка","Предзаказ"],state=States.waiting_for_type)
async def order_type(message: types.Message,state):
    flag = False
    user_data = await state.get_data()
    if not user_data.get("order_flag",True):
        order_info = Order.get_by_id(user_data["order_id"]).order
    else:
        order_info = user_data["basket"]
    for element in order_info:
        if not element["is_package"]:
            product = Post.get_by_id(element["id"])
            if not product.is_available:
                flag = True
                break
    if message.text == "Самовывоз":
        if not flag:
            await state.update_data(delivery_type=1)
            await States.waiting_for_time.set()
            await message.answer("Какое время вам удобно? Нажмите или введите",reply_markup=kb.time_kb)
        else:
            await message.answer("В вашей корзине есть товары, для которых доступен только предзаказ")
    elif message.text == "Доставка":
        if not flag:
            await state.update_data(delivery_type=2)
            await States.waiting_for_time.set()
            await message.answer("Какое время вам удобно? Нажмите или введите",reply_markup=kb.time_kb)
        else:
            await message.answer("В вашей корзине есть товары, для которых доступен только предзаказ")
    else:
        Order.create(
            user = User.get(User.user_id == message.from_user.id),
            order_created = datetime.datetime.now(),
            order = user_data["basket"],
            status = 1,
            order_summ = sum(elem.get("cost",0) for elem in user_data["basket"]),
            longitude = None,
            latitude = None,
            client_asked_time = None,
            order_type = 3
        )
        await state.update_data(
            location={},
            basket=[],
            delivery_type=None,
            time=None,
            money_type=None,
            system=None,
            payment_type=None,
            order_flag = True
            )
        await message.answer("Ваш предзаказ сформирован. Когда он появится, вы получите уведомление.",reply_markup=kb.start_kb(message.from_user.id))
        await States.main_menu.set()


@dp.message_handler(lambda message: message.text!="Назад",state=States.waiting_for_time)
async def order_time(message: types.Message, state):
    user_data = await state.get_data()
    if message.text == "Ближайшее время":
        await state.update_data(time=message.text)
        if user_data["delivery_type"] == 1:
            await States.waiting_for_money_type.set()
            await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)
        elif user_data["delivery_type"] == 2:
            await States.waiting_for_location.set()
            await message.answer("Отправьте локацию или выберите из списка",reply_markup=kb.locations_kb(message.from_user.id))
    else:
        if re.fullmatch(r"[0-2][0-9]:[0-5][0-9]",message.text) is None:
            await message.answer("Неверный формат времени. Ожидается hh:mm")
        else:
            await state.update_data(time=message.text)
            if user_data["delivery_type"] == 1:
                await States.waiting_for_money_type.set()
                await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)
            elif user_data["delivery_type"] == 2:
                await States.waiting_for_location.set()
                await message.answer("Отправьте локацию или выберите из списка",reply_markup=kb.locations_kb(message.from_user.id))

@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=States.waiting_for_location)
async def get_location(message: types.Message,state):
    await state.update_data(
        location={
            "longitude":message.location.longitude,
            "latitude":message.location.latitude
        }
        )
    await States.waiting_for_money_type.set()
    await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)

@dp.message_handler(lambda message: message.text != "Назад", state=States.waiting_for_location)
async def get_location(message: types.Message,state):
    user = User.get(User.user_id==message.from_user.id)
    for location in user.locations:
        if location["name"] == message.text:
            await state.update_data(
                location={
                    "longitude":location["longitude"],
                    "latitude":location["latitude"]
                }
                )
            await States.waiting_for_money_type.set()
            await message.answer("Выберите тип оплаты",reply_markup=kb.money_kb)
            break

@dp.message_handler(lambda message: message.text != "Назад", state=States.waiting_for_money_type)
async def get_money_type(message:types.Message,state):
    if (message.text == "Наличные" or message.text == "Карта") and message.text!="Назад":
        user_data = await state.get_data()
        await state.update_data(money_type=message.text)
        if message.text == "Карта":
            await message.answer("Выберите платежную систему",reply_markup=kb.system_type_kb)
            await States.select_system_type.set()
        else:
            text = "Ваш заказ:\n"
            if not user_data.get("order_flag",True):
                order_info = Order.get_by_id(user_data["order_id"]).order
            else:
                order_info = user_data["basket"]
            order_data = create_order_list(order_info)
            for data in order_data:
                text+=f"{data['name']} {data['ammount']} cум\n"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row("Подтвердить","Отменить")
            await message.answer(text,reply_markup=keyboard)
            await States.waiting_for_approve.set()
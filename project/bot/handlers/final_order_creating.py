from aiogram import types
from admin_bot.bot_class import bot as admin_bot
from bot.bot_class import dp, bot
from bot.states import States
import bot.keyboards as kb
from functions import create_order_list
from models import Order, User, SuperUser
import datetime
tokens={
    "Click":"398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065",
    "Payme":"371317599:TEST:1603623216394"
}

@dp.message_handler(text="Отменить",state=States.waiting_for_approve)
async def cancel_order(message: types.Message,state):
    await message.answer("Главное меню",reply_markup=kb.start_kb(message.from_user.id))
    await States.main_menu.set()

@dp.message_handler(text="Подтвердить",state=States.waiting_for_approve)
async def close_order(message:types.Message,state):
    user_data = await state.get_data()
    if user_data.get("money_type") == "Карта":
        if user_data.get("payment_type") == "Через телеграм":
            products = []
            order_data = create_order_list(user_data["basket"])
            for element in order_data:
                products.append(
                    types.LabeledPrice(
                        label = element["name"],
                        amount=int(element["ammount"])*100
                    )
                )
            await bot.send_invoice(
                message.from_user.id,
                title="Тестовый платеж",
                description="Тестируем функцию оплаты",
                provider_token=tokens[user_data["system"]],
                currency='UZS',
                is_flexible=False,  # True если конечная цена зависит от способа доставки
                prices=products,
                start_parameter='time-machine-example',
                payload='some-invoice-payload-for-our-internal-use',
                need_phone_number = True,
                send_phone_number_to_provider = True,
                reply_markup=kb.start_kb(message.from_user.id)
            )
        else:
            if not user_data.get("order_flag",True):
                order = Order.get(Order.id == user_data["order_id"])
                order.status = 2
                order.longitude = user_data["location"].get("longitude",None) if "location" in user_data else None
                order.latitude = user_data["location"].get("latitude",None) if "location" in user_data else None
                order.client_asked_time = user_data["time"]
                order.order_type = user_data["delivery_type"]
                order.payment_dop_info = user_data["system"]
                order.save()
            else:
                Order.create(
                    user = User.get(User.user_id == message.from_user.id),
                    order_created = datetime.datetime.now(),
                    order = user_data["basket"],
                    status = 2,
                    order_summ = sum(elem.get("cost",0) for elem in user_data["basket"]),
                    longitude = user_data["location"].get("longitude",None) if "location" in user_data else None,
                    latitude = user_data["location"].get("latitude",None) if "location" in user_data else None,
                    client_asked_time = user_data["time"],
                    order_type = user_data["delivery_type"],
                    payment_status = 0,
                    payment_dop_info = user_data["system"]
                )

            await message.answer("Ваш заказ сформирован. Оплатите его.",reply_markup=kb.start_kb(message.from_user.id))
            await States.main_menu.set()
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
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Отправить ссылку для оплаты",callback_data=f"payment_{message.from_user.id}_{order.id}")
            keyboard.row(btn)
            text = f"Создан заказ № {order.id}.\nПользователь хочет оплатить его через {user_data['system']}. Пожалуйста, нажмите на кнопку и отправьте ссылку для оплаты\nСумма заказа: {order.order_summ}"
            for superuser in SuperUser.select():
                await admin.send_message(superuser.user_id,text,reply_markup=keyboard)
    else:
        print(user_data.get("order_flag",True))
        if not user_data.get("order_flag",True):
            order = Order.get(Order.id == user_data["order_id"])
            order.status = 2
            order.longitude = user_data["location"].get("longitude",None) if "location" in user_data else None
            order.latitude = user_data["location"].get("latitude",None) if "location" in user_data else None
            order.client_asked_time = user_data["time"]
            order.order_type = user_data["delivery_type"]
            order.payment_status = 1
            order.save()
        else:
            Order.create(
                user = User.get(User.user_id == message.from_user.id),
                order_created = datetime.datetime.now(),
                order = user_data["basket"],
                status = 2,
                order_summ = sum(elem.get("cost",0) for elem in user_data["basket"]),
                longitude = user_data["location"].get("longitude",None) if "location" in user_data else None,
                latitude = user_data["location"].get("latitude",None) if "location" in user_data else None,
                client_asked_time = user_data["time"],
                order_type = user_data["delivery_type"],
                payment_status = 1
            )
        await message.answer("Ваш заказ сформирован. С вами свяжутся",reply_markup=kb.start_kb(message.from_user.id))
        await States.main_menu.set()
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

@dp.pre_checkout_query_handler(state="*")
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=types.successful_payment)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,"Оплата принята"
    )
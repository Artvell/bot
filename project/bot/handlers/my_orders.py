from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
from functions import create_order_list
from bot.keyboards import order_list_kb
from models import Order, Post
from functions import Formatter
import emoji

@dp.message_handler(text="Мои заказы", state=States.main_menu)
async def order_type(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Назад")
    kb.row("Ожидают оплаты","Выполняются")
    kb.row("Предзаказ", "Закрытые")
    await message.answer(
        "Выберите тип заказа",
        reply_markup=kb
        )
    await States.waiting_for_order_type.set()

@dp.message_handler(lambda message: message.text in ("Выполняются","Предзаказ", "Закрытые","Ожидают оплаты"),state=States.waiting_for_order_type)
async def orders_list(message: types.Message,state):
    await message.answer("Выберите заказ из списка",reply_markup=order_list_kb(message.text, message.from_user.id))
    await state.update_data(order_type=message.text)
    await States.orders_list.set()

@dp.message_handler(lambda message: message.text.startswith("Заказ"),state=States.orders_list)
async def order_info(message: types.Message, state):
    data = message.text.split()
    if len(data) == 2:
        order_id = data[1]
        order = Order.get_or_none(Order.id == order_id)
        if order is None:
            await message.answer(
                "Некорректные данные",
                reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад")
                )
        else:
            status = {
                1:"Предзаказ",
                2:"Выполняется",
                3:"Закрыт",
                4:"Ожидает оплаты"
            }
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("Назад")
            await state.update_data(order_id=order_id)
            if order.status != 1:
                text = f"""Заказ №{order.id}
                Открыт: {order.order_created}
                Текущий статус: {status[order.status]}
                Тип: {"Доставка" if order.longitude is not None else "Самовывоз"}
                Запрошенное время: {order.client_asked_time}
                Общая сумма заказа: {order.order_summ} сум

                <b>Подробнее о заказе:</b>
                """
                if order.status == 4:
                    keyboard.add("Запросить ссылку для оплаты")
            else:
                text = f"""Заказ №{order.id}
                Открыт: {order.order_created}
                Текущий статус: {status[order.status]}
                Общая сумма заказа: {order.order_summ} сум

                <b>Подробнее о заказе:</b>
                """
                keyboard.add("Уточнить наличие")
            for element in order.order:
                product = Post.get(Post.id == element["id"])
                name = f'<a href="{product.telegraph}">{Formatter(product).get_name()}</a>'
                text+=f"{name} {element['kol']} {int(element['kol'])*product.cost} сумов\n"
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            await States.order_info.set()
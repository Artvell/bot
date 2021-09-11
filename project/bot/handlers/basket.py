import emoji
from tabulate import tabulate
from aiogram import types
from bot.bot_class import dp,bot
from bot import States
from models import Post, Package
from functions import Formatter
from bot.keyboards import basket_kb

@dp.callback_query_handler(text="basket",state=States.main_menu)
async def basket(callback_query=None,state=None,chat_id=None):
    user_data = await state.get_data()
    basket = user_data.get("basket", None)
    if basket is None or len(basket)==0:
        if chat_id is None:
            await callback_query.answer("Корзина пуста",show_alert=True)
        else:
            await bot.send_message(chat_id,"Корзина пуста")
    else:
        if callback_query is not None:
            await bot.delete_message(
                callback_query.from_user.id,
                callback_query.message.message_id,
            )
        all_summ = 0
        data = []
        text="{:<10} {:<5} {:<5}\n".format('Название','Кол-во','Сумма')
        for elem in basket:
            if elem.get("is_package",False):
                package = Package.get_by_id(elem["id"])
                text += f'{package.title} 1 {package.cost}\n'
                all_summ += package.cost
                data.append(
                    {
                        "is_package": True,
                        "id":elem["id"],
                        "name":package.title
                    }
                )
            else:
                product = Post.get(Post.id==elem["id"])
                name = Formatter(product).get_name()
                summ = int(elem["kol"])*product.cost
                text += '<a href="{}">{}</a> {} {} сум\n'.format(product.telegraph,name,elem["kol"],summ)
                all_summ += int(summ)
                data.append(
                    {
                        "is_package": False,
                        "id":elem["id"],
                        "name":name
                    }
                )
        text+=f"Итого: {all_summ} сум"
        if chat_id is None:
            chat_id = callback_query.from_user.id
            #await message.answer(text,parse_mode="HTML",disable_web_page_preview=True,reply_markup=basket_kb(data))
        await bot.send_message(chat_id,text,parse_mode="HTML",disable_web_page_preview=True,reply_markup=basket_kb(data))

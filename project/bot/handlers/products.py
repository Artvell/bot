"""Из старой вернсии, для пролистывания всех товаров. Работает, но убран из бота
Чтобы вернуть, в файле keyboards/inline_menu_kb.py расскомментируйте 5 и 9 строки"""
from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
from functions import create_product_message
from bot.keyboards import product_kb
from models import Post

@dp.callback_query_handler(text="products",state=States.main_menu)
async def product(message: types.Message, state):
    user_data = await state.get_data()
    prev_id = user_data.get("selected_id",None)
    await state.update_data(filter={})
    if prev_id is None:
        product,caption,prod_id = create_product_message()
        await bot.send_photo(message.from_user.id,product,caption,reply_markup=product_kb,parse_mode="HTML")
        await state.update_data(prev_id=prod_id)
    else:
        product,caption,prod_id = create_product_message(prev_id)
        await bot.send_photo(message.from_user.id,product,caption,reply_markup=product_kb,parse_mode="HTML")
    await state.update_data(selected_id=prod_id)
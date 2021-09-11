import emoji
from tabulate import tabulate
from aiogram import types
from bot.bot_class import dp, bot
from bot import States
from models import Post, BasketClearingStats, BasketStats, Package
from functions import Formatter
from bot.keyboards import basket_kb
from bot.handlers.basket import basket

@dp.callback_query_handler(text="clear_basket",state=States.main_menu)
async def clear_basket(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data(basket=[])
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "Корзина очищена")
    deleted_stats, created = BasketClearingStats.get_or_create(user_id=callback_query.from_user.id)
    if not created:
        deleted_stats.counter += 1
        deleted_stats.save()

@dp.callback_query_handler(lambda query: query.data.startswith("delete_"),state=States.main_menu)
async def delete_product_from_basket(callback_query: types.CallbackQuery, state):
    await bot.answer_callback_query(callback_query.id)
    print(callback_query.data)
    user_data = await state.get_data()
    product_id = callback_query.data.split("_")[1]
    is_package = True if callback_query.data.split("_")[2] == "1" else False
    products = user_data["basket"]
    new_products = []
    for product in products:
        print(product["id"],product_id,"|",product["is_package"],is_package)
        if product["id"] == product_id and product["is_package"] == is_package:
            continue
        else:
            new_products.append(product)
    await state.update_data(basket=new_products)
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await basket(state=state,message=None,chat_id=callback_query.from_user.id)
    if is_package:
        package = Package.get_by_id(product_id)
        basket_stats,created = BasketStats.get_or_create(product_name=package.title,type=False)
        if not created:
            basket_stats.counter += 1
            basket_stats.save()
    else:
        product = Post.get_by_id(product_id)
        basket_stats,created = BasketStats.get_or_create(product_name=product.name,type=True)
        if not created:
            basket_stats.counter += 1
            basket_stats.save()

    

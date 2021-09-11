from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
from functions import create_product_message, is_user_exists, create_text
from bot.keyboards import product_kb, numbers_kb
from models import Post, Package, ProductsInPackage, BasketStats

@dp.callback_query_handler(text="Корзина", state="*")
async def open_numbers(callback_query: types.CallbackQuery,state):
    if is_user_exists(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id)
        user_data = await state.get_data()
        prod_id = user_data["selected_id"]
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=numbers_kb(prod_id)
        )
    else:
        await bot.answer_callback_query(callback_query.id,"Вы не зарегистрированы!")

@dp.callback_query_handler(text="❌", state="*")
async def close_numbers(callback_query: types.CallbackQuery,state):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=product_kb
    )

@dp.callback_query_handler(lambda btn: btn.data.startswith("product"),state="*")
async def add_to_basket(callback_query: types.CallbackQuery,state):
    user_data = await state.get_data()
    basket = user_data.get("basket",None)
    print(callback_query.data)
    product_data = callback_query.data.split("_")[1::]
    print(product_data)
    product = Post.get(Post.id==product_data[0])
    packages = ProductsInPackage.select().where(ProductsInPackage.product == product.id)
    if packages.count() > 0 and len(product_data) == 2:
        package = packages[0]
        text = "Спецпредложение\n"
        pack_text = text+create_text(package.package.id)
        keyboard = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Принять", callback_data=f"package_to_basket_{package.package.id}_{product.id}:{product_data[1]}")
        btn2 = types.InlineKeyboardButton("Отказаться", callback_data=f"{callback_query.data}_no")
        keyboard.row(btn1,btn2)
        await bot.send_message(
            callback_query.from_user.id,
            pack_text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    else:
        if basket is None:
            data = [
                {
                    "is_package":False,
                    "id":product_data[0],
                    "kol":product_data[1],
                    "cost":product.cost
                }
            ]
            await state.update_data(basket=data)
        else:
            basket.append(
                {
                    "is_package":False,
                    "id":product_data[0],
                    "kol":product_data[1],
                    "cost": product.cost
                } 
            )
            await state.update_data(basket=basket)
        basket_stats,created = BasketStats.get_or_create(product_name=product.name,type=True)
        if not created:
            basket_stats.counter += 1
            basket_stats.save()
    await bot.answer_callback_query(callback_query.id,"Товар добавлен в корзину")
    if product_data[-1] == "no":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    else:
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=product_kb
        )


@dp.callback_query_handler(lambda btn: btn.data.startswith("package_to_basket_"),state="*")
async def add_package_to_basket(callback_query: types.CallbackQuery, state):
    user_data = await state.get_data()
    package_id = callback_query.data.split("_")[-2]
    product_info = callback_query.data.split("_")[-1].split(":")
    package = Package.get_by_id(package_id)
    basket = user_data.get("basket",None)
    if basket is None:
        data = [
            {
                "is_package":True,
                "id":package_id,
                "kol":1,
                "cost":package.cost
            }
        ]
        await state.update_data(basket=data)
    else:
        basket.append(
            {
                "is_package":True,
                "id":package_id,
                "kol":1,
                "cost":package.cost
            } 
        )
        await state.update_data(basket=basket)
    print(package, package.title)
    basket_stats,created = BasketStats.get_or_create(product_name=package.title,type=True)
    if not created:
        basket_stats.counter += 1
        basket_stats.save()
    if int(product_info[1]) > 1:
        basket = user_data.get("basket",None)
        product = Post.get_by_id(product_info[0])
        basket.append(
            {
                "is_package":False,
                "id":product.id,
                "kol":int(product_info[1])-1,
                "cost":product.cost
            } 
        )
        await state.update_data(basket=basket)
        basket_stats,created = BasketStats.get_or_create(product_name=product.name,type=True)
        if not created:
            basket_stats.counter += 1
            basket_stats.save()
    await bot.answer_callback_query(callback_query.id,"Товар добавлен в корзину")
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
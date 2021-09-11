from aiogram import types
from bot.bot_class import dp, bot
from bot.keyboards import category_kb,subcategories_kb, product_kb
from bot.states import States
from models import Category, Subcategory, CategStats
from functions import product_message_by_category

@dp.callback_query_handler(state=States.main_menu,text="categories")
async def categories(callback_query: types.CallbackQuery,state):
    await States.waiting_for_subcategory.set()
    await bot.edit_message_text(
        "Категории",
        callback_query.from_user.id,
        callback_query.message.message_id,
        reply_markup=category_kb
        )

@dp.callback_query_handler(
    lambda message: message.data in [c.category for c in Category.select()],
    state=States.waiting_for_subcategory
    )
async def subcategories(callback_query: types.Message,state):
    print("hey")
    subcategories = Subcategory.select(Subcategory,Category).join(Category).where(Category.category == callback_query.data)
    category = Category.get(Category.category == callback_query.data)
    print(category)
    stats,created = CategStats.get_or_create(name=category.category)
    if not created:
        stats.counter += 1
        stats.save()
    if subcategories.count()>0:
        await callback_query.answer()
        await States.subcategories.set()
        await state.update_data(category = category.id)
        await bot.edit_message_text(
            "Подкатегории",
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=subcategories_kb(subcategories)
        )
        #await bot.send_message(callback_query.from_user.id,message.text,reply_markup=subcategories_kb(subcategories))
    else:
        user_data = await state.get_data()
        photo,caption,prod_id = product_message_by_category(category.id,True)
        if photo is not False:
            await bot.send_photo(callback_query.from_user.id,photo,caption,reply_markup=product_kb,parse_mode="HTML")
            await state.update_data(
                prev_param_id=prod_id,
                filter={
                    "flag":True,
                    "parameter": category.id
                },
                selected_id=prod_id
            )
        else:
            await callback_query.answer("Здесь пока ничего нет",show_alert=True)

@dp.callback_query_handler(
    lambda message: message.data in [s.subcategory for s in Subcategory.select()],
    state=States.subcategories
    )
async def by_subcategories(callback_query: types.CallbackQuery,state):
    user_data = await state.get_data()
    subcategory = Subcategory.get((Subcategory.category==user_data["category"])&(Subcategory.subcategory==callback_query.data))
    print(subcategory)
    stats,created = CategStats.get_or_create(name=f"{subcategory.category.category}/{subcategory.subcategory}")
    if not created:
        stats.counter += 1
        stats.save()
    photo,caption,prod_id = product_message_by_category(subcategory.id,False)
    print(photo)
    if photo is not False:
        await bot.send_photo(callback_query.from_user.id,photo,caption,reply_markup=product_kb,parse_mode="HTML")
        await state.update_data(
            prev_param_id=prod_id,
            filter={
                "flag":False,
                "parameter": subcategory.id
            },
            selected_id=prod_id
        )
    else:
        await callback_query.answer("Здесь пока ничего нет",show_alert=True)
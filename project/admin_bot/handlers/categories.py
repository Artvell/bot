from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.keyboards import category_keyboard,subcategories_keyboard, product_keyboard
from admin_bot.states import States
from models import Category, Subcategory
from functions import product_message_by_category

@dp.message_handler(state=States.main_menu,text="Категории")
async def categories(message: types.Message,state):
    await States.waiting_for_subcategory.set()
    await bot.send_message(message.from_user.id,"Категории", reply_markup=category_keyboard)

@dp.message_handler(
    lambda message: message.text in [c.category for c in Category.select()],
    state=States.waiting_for_subcategory
    )
async def subcategories(message: types.Message,state):
    subcategories = Subcategory.select(Subcategory,Category).join(Category).where(Category.category == message.text)
    category = Category.get(Category.category == message.text)
    if subcategories.count()>0:
        await States.subcategories.set()
        await state.update_data(category = category.id)
        await bot.send_message(message.from_user.id,message.text,reply_markup=subcategories_keyboard(subcategories))
    else:
        user_data = await state.get_data()
        photo,caption,prod_id = product_message_by_category(category.id,True)
        if photo is not False:
            await message.answer_photo(photo,caption,reply_markup=product_keyboard(flag=True),parse_mode="HTML")
            await state.update_data(
                prev_param_id=prod_id,
                filter={
                    "flag":True,
                    "parameter": category.id
                },
                selected_id=prod_id
            )
        else:
            await message.answer("Здесь пока ничего нет")

@dp.message_handler(
    lambda message: message.text in [s.subcategory for s in Subcategory.select()],
    state=States.subcategories
    )
async def by_subcategories(message: types.Message,state):
    user_data = await state.get_data()
    subcategory = Subcategory.get((Subcategory.category==user_data["category"])&(Subcategory.subcategory==message.text))
    photo,caption,prod_id = product_message_by_category(subcategory.id,False)
    if photo is not False:
        await message.answer_photo(photo,caption,reply_markup=product_keyboard(True),parse_mode="HTML")
        await state.update_data(
            prev_param_id=prod_id,
            filter={
                "flag":False,
                "parameter": subcategory.id
            },
            selected_id=prod_id
        )
    else:
        await message.answer("Здесь пока ничего нет")
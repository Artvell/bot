from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from functions import create_product_message, is_superuser
from admin_bot.keyboards import product_keyboard, category_kb, subcategories_kb
from models import Post, Subcategory, Category

@dp.callback_query_handler(text="link", state="*")
async def open_categories(callback_query: types.CallbackQuery,state):
    await bot.answer_callback_query(callback_query.id)
    if is_superuser(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=category_kb
        )
    else:
        await bot.answer_callback_query(callback_query.id,"Вы не зарегистрированы!")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("category_"), state="*")
async def open_subcategories(callback_query: types.CallbackQuery,state):
    categ_id = callback_query.data.split("_")[1]
    subcategories = Subcategory.select(Subcategory,Category).join(Category).where(Category.id == categ_id)
    if subcategories.count()>0:
        await bot.answer_callback_query(callback_query.id)
        await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=subcategories_kb(subcategories)
        )
    else:
        user_data = await state.get_data()
        prod_id = user_data["selected_id"]
        post = Post.get(Post.id==prod_id)
        post.category = Category.get_by_id(categ_id)
        post.save()
        product,caption,prod_id = create_product_message(prod_id)
        caption += f"\nКатегория: {post.category.category}"
        await bot.edit_message_caption(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=product_keyboard(True)
        )
        await bot.answer_callback_query(callback_query.id,"Товар привязан к категории")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("subcateg_"), state="*")
async def link(callback_query: types.CallbackQuery,state):
    subcateg_id = callback_query.data.split("_")[1]
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    subcateg = Subcategory.get(Subcategory.id==subcateg_id)
    post = Post.get(Post.id==prod_id)
    post.subcategory = subcateg
    post.category = subcateg.category
    post.save()
    product,caption,prod_id = create_product_message(prod_id)
    caption += f"\nКатегория: {post.subcategory.category.category}\nПодкатегория: {post.subcategory.subcategory}"
    await bot.edit_message_caption(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=product_keyboard(True, post.is_available)
    )
    await bot.answer_callback_query(callback_query.id,"Товар привязан к подкатегории")

@dp.callback_query_handler(text="❌", state="*")
async def close_links(callback_query: types.CallbackQuery,state):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    post = Post.get_by_id(prod_id)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=product_keyboard(is_available=post.is_available)
    )

@dp.callback_query_handler(text="unlink", state="*")
async def unlink(callback_query: types.CallbackQuery,state):
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    post = Post.get_by_id(prod_id)
    post.category = None
    post.subcategory = None
    post.save()
    await bot.answer_callback_query(callback_query.id,"Товар отвязан")
    product,caption,prod_id = create_product_message(prod_id)
    await bot.edit_message_caption(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=product_keyboard(is_available=post.is_available)
    )
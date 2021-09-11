from aiogram import types
from admin_bot.bot_class import dp
from admin_bot.states import States
from functions import create_product_message
from admin_bot.keyboards import product_keyboard
from models import Post

@dp.message_handler(text="Товары",state=States.main_menu)
async def product(message: types.Message, state):
    user_data = await state.get_data()
    prev_id = user_data.get("selected_id",None)
    await state.update_data(filter={})
    flag = False
    if prev_id is None:
        product,caption,prod_id = create_product_message(is_superuser=True)
        await state.update_data(selected_id=prod_id)
        await state.update_data(prev_id=prod_id)
    else:
        product,caption,prod_id = create_product_message(prev_id,is_superuser=True)
    post = Post.get_by_id(prod_id)
    if post.subcategory is not None:
        flag = True
        caption += f"\nКатегория: {post.subcategory.category.category}\nПодкатегория: {post.subcategory.subcategory}"
    elif post.category is not None:
        flag = True
        caption += f"\nКатегория: {post.category.category}"
    await message.answer_photo(product,caption,reply_markup=product_keyboard(flag, post.is_available,post.is_visible),parse_mode="HTML")
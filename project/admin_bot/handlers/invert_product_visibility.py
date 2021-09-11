from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from functions import create_product_message
from admin_bot.keyboards import product_keyboard
from models import Post

@dp.callback_query_handler(text="invert_visibility", state="*")
async def invert_visiblity(callback_query: types.CallbackQuery, state):
    await callback_query.answer()
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    post = Post.get_by_id(prod_id)
    post.is_visible = not post.is_visible
    post.save()
    product,caption,prod_id = create_product_message(prod_id)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=product_keyboard(True,post.is_available, post.is_visible)
    )
    await callback_query.answer("Изменено")
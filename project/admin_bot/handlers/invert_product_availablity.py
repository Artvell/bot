from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from functions import create_product_message
from admin_bot.keyboards import product_keyboard
from models import Post

@dp.callback_query_handler(text="invert_availabl", state="*")
async def invert(callback_query: types.CallbackQuery, state):
    await callback_query.answer()
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    post = Post.get_by_id(prod_id)
    post.is_available = not post.is_available
    post.save()
    product,caption,prod_id = create_product_message(prod_id)
    await bot.edit_message_caption(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=product_keyboard(True,post.is_available)
    )
    await callback_query.answer("Изменено")
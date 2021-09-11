from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
from functions import create_product_message, product_message_by_category
from bot.keyboards import product_kb
from models import CategStats


@dp.callback_query_handler(text="Следующий", state="*")
@dp.callback_query_handler(text="Предыдущий", state="*")
async def rotate_btn(callback_query: types.CallbackQuery,state):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    prev_id = user_data.get("prev_id",None)
    prev_param_id = user_data.get("prev_param_id",None)
    filter_info = user_data.get("filter",None)
    if callback_query.data == "Предыдущий":
        if (filter_info is not None) and (filter_info != {}):
            product,caption,prod_id = product_message_by_category(filter_info["parameter"],filter_info["flag"],prev_param_id,False)
        else:
            product,caption,prod_id = create_product_message(prev_id, False)
    else:
        if (filter_info is not None) and (filter_info) != {}:
            product,caption,prod_id = product_message_by_category(filter_info["parameter"],filter_info["flag"],prev_param_id,True)
        else:
            product,caption,prod_id = create_product_message(prev_id, True)
    if product is not False:
        new_photo = types.InputMediaPhoto(media=product,caption=caption,parse_mode="HTML")
        await bot.edit_message_media(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            media = new_photo,
            reply_markup=product_kb
        )
        if filter_info is not None and filter_info != {}:
            await state.update_data(prev_param_id=prod_id)
        else:
            await state.update_data(prev_id=prod_id)
        await state.update_data(selected_id=prod_id)
from aiogram import types
from bot.bot_class import dp, bot
from bot.states import States
import bot.keyboards as kb
from bot.handlers import basket

@dp.callback_query_handler(text="back",state="*")
async def inline_back(callback_query: types.CallbackQuery, state):
    current_state = await state.get_state()
    if current_state == States.waiting_for_subcategory.state:
        await bot.edit_message_text(
            "⁣⁣⁣⁣⁣⁣⁣            Главное меню          ",
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=kb.menu_kb()
            )
        await States.main_menu.set()
    elif current_state == States.subcategories.state:
        await bot.edit_message_text(
            "Категории",
            callback_query.from_user.id,
            callback_query.message.message_id,
            reply_markup=kb.category_kb
        )
        await States.waiting_for_subcategory.set()

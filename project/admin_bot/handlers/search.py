from aiogram import types
from admin_bot.bot_class import dp
from admin_bot.states import States

@dp.message_handler(state=States.main_menu,text="Поиск")
async def search_handler(message: types.Message,state):
    await message.answer(
        "Нажмите на кнопку и впишите название/описание товара",
        reply_markup=types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton(
                "Поиск",
                switch_inline_query_current_chat=""
            )
        )
    )
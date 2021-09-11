from aiogram import types
from admin_bot.bot_class import dp,bot
from admin_bot.states import States
from admin_bot.keyboards import start_kb
from functions import is_superuser


@dp.message_handler(commands=['start'], state = "*")
async def cmd_start(message: types.Message, state):
    if is_superuser(message.from_user.id):
        await States.main_menu.set()
        await message.answer("Здравствуйте, администратор",reply_markup=start_kb())
    else:
        await message.answer("Вы не администратор!")


@dp.message_handler(commands=["reset"], state=States.main_menu)
async def reset(message: types.Message, state):
    await state.update_data(
        prev_id = None,
        prev_param_id = None,
        selected_id = None
    )
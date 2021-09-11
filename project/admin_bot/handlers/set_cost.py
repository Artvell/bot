from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from models import Post

@dp.callback_query_handler(text="set_cost", state="*")
async def set_cost(callback_query: types.CallbackQuery,state):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Введите цену")
    cur_state = await state.get_state()
    await state.update_data(prev_state=cur_state)
    await States.waiting_for_cost.set()

@dp.message_handler(lambda message: message.text.isdigit(),state=States.waiting_for_cost)
async def new_cost(message: types.Message,state):
    user_data = await state.get_data()
    prod_id = user_data["selected_id"]
    post = Post.get_by_id(prod_id)
    post.cost = message.text
    post.save()
    await state.set_state(user_data["prev_state"])
    await message.answer("Цена установлена")
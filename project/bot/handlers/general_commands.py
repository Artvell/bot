from aiogram import types
from bot.bot_class import dp,bot
from bot.states import States
from bot.keyboards import start_kb
from functions import is_user_exists, create_media_list
from models import Story, UserGrowth
from datetime import datetime
from datetime import date as dt

    
@dp.message_handler(commands=['start'], state = "*")
async def cmd_start(message: types.Message, state):
    stories = Story.select().where(Story.expiry_time>datetime.timestamp(datetime.now())).order_by(Story.id.desc()).limit(3)
    if stories.count()==0:
        for media_list in create_media_list():
            await bot.send_media_group(message.from_user.id, media_list)
    else:
        for story in stories[::-1]:
            if story.type == 2:
                await bot.send_video(message.from_user.id,story.link)
            elif story.type == 1:
                await bot.send_photo(message.from_user.id, story.link)
    if is_user_exists(message.from_user.id):
        await States.main_menu.set()
        await message.answer("Снова здравствуйте",reply_markup=start_kb(message.from_user.id))
    else:
        await States.waiting_for_number.set()
        await message.answer("Здравствуйте. Отправьте свой номер телефона",reply_markup=start_kb(message.from_user.id))
        stats,created = UserGrowth.get_or_create(date=dt.today())
        if not created:
            stats.counter += 1
            stats.save()


@dp.message_handler(commands=["reset"], state=States.main_menu)
async def reset(message: types.Message, state):
    await state.reset_data()
from aiogram import types
from bot.bot_class import dp
from bot import States
from models import User
@dp.message_handler(content_types=types.ContentTypes.CONTACT, state = States.waiting_for_number)
async def contact_messages(message: types.Message):
    user, created = User.get_or_create(
                        user_id = message.contact.user_id,
                        username = message.from_user.username,
                        full_name = message.from_user.full_name,
                        phone = message.contact.phone_number
                        )
    await States.main_menu.set()
    if created:
        await message.answer("Спасибо. Вы зарегистрированы")
    else:
        await message.answer("Снова здравствуйте")
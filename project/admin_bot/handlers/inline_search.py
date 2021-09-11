import hashlib
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from admin_bot.keyboards import product_keyboard, start_kb
from aiogram import types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from models import Post
from functions import Formatter, create_product_message,is_superuser
from emoji import emojize
from uuid import uuid4



@dp.inline_handler(state="*")
async def inline_search(inline_query: InlineQuery,state):
    if is_superuser(inline_query.from_user.id):
        user_data = await state.get_data()
        text = inline_query.query
        if text:
            products = Post.select().order_by(Post.id.desc()).where(Post.text.contains(text))
            results = []
            for product in products:
                input_content = InputTextMessageContent(product.id)
                formatter = Formatter(product)
                item = InlineQueryResultArticle(
                    id=str(uuid4()),
                    url = product.links[0],
                    thumb_url = product.links[0],
                    title=formatter.get_name(),
                    description=str(product.cost)+" сум",
                    input_message_content=input_content,
                    hide_url=True
                )
                results.append(item)
                if len(results)>20:
                    break
            current_state = await state.get_state()
            if current_state!=States.searching.state:
                await state.update_data(prev_state=current_state)
            await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)
            if user_data.get("adding",False):
                await States.adding_products_to_package.set()
            else:
                await States.searching.set()
        else:
            user_data = await state.get_data()
            await state.set_state(user_data["prev_state"])


@dp.message_handler(content_types=types.ContentTypes.TEXT, state = States.searching)
async def search_result(message:types.Message,state):
    user_data = await state.get_data()
    current_state = await state.get_state()
    if message.text.isdigit():
        product,caption,prod_id = create_product_message(message.text)
        post = Post.get_by_id(prod_id)
        if product is None:
            await message.answer("Ничего не найдено")
        else:
            await message.delete()
            if (post.category is None) and (post.subcategory is None):
                await message.answer_photo(product,caption,reply_markup=product_keyboard(),parse_mode="HTML")
            else:
                if post.subcategory is not None:
                    caption += f"\nКатегория: {post.subcategory.category.category}\nПодкатегория: {post.subcategory.subcategory}"
                elif post.category is not None:
                    caption += f"\nКатегория: {post.category.category}"
                await message.answer_photo(product,caption,reply_markup=product_keyboard(True),parse_mode="HTML")
            await state.update_data(selected_id=message.text)
        await state.set_state(user_data["prev_state"])
    else:
        await States.main_menu.set()
        await message.answer("Главное меню",reply_markup=start_kb())
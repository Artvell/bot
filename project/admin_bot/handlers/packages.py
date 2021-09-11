from aiogram import types
from admin_bot.bot_class import dp, bot
from admin_bot.states import States
from admin_bot.keyboards import package_kb, adding_kb, start_kb
from functions import create_text
from models import Package, Post, ProductsInPackage
import re

@dp.message_handler(text="Пакеты",state=States.main_menu)
async def packages_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Создать пакет", callback_data="create_package"))
    keyboard.add(types.InlineKeyboardButton("Все пакеты", callback_data="show_packages"))
    await message.answer("Выберите действие",reply_markup=keyboard)

@dp.callback_query_handler(text="create_package", state=States.main_menu)
async def create_package(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(
        callback_query.from_user.id,
        "Введите название пакета",
        reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Назад")
    )
    await States.waiting_for_package_title.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=States.waiting_for_package_title)
async def set_package_title(message: types.Message):
    package = Package.create(title = message.text)
    text = create_text(package.id)
    await message.answer("Успешно!",reply_markup=start_kb())
    await message.answer(text,reply_markup=package_kb(package.id),parse_mode="HTML",disable_web_page_preview=True)
    await States.main_menu.set()

@dp.callback_query_handler(lambda callback:callback.data.startswith("delete_package_"), state=States.main_menu)
async def delete_package(callback_query: types.CallbackQuery):
    package_id = callback_query.data.split("_")[-1]
    package = Package.get_or_none(Package.id == package_id)
    if package is not None:
        ProductsInPackage().delete().where(ProductsInPackage.package == package.id).execute()
        package.delete_instance()
        await callback_query.answer("Пакет удален",show_alert=True)
    else:
        await callback_query.answer("Этого пакета уже не существует",show_alert=True)
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)

@dp.callback_query_handler(text="show_packages", state=States.main_menu)
async def show_packages(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    packages = Package.select()
    if packages.count() > 0:
        await callback_query.answer()
        for package in packages:
            btn = types.InlineKeyboardButton(package.title,callback_data=f"package_{package.id}")
            keyboard.row(btn)
        await bot.send_message(
            callback_query.from_user.id,
            "Ваши пакеты",
            reply_markup=keyboard
        )
    else:
        await callback_query.answer("Пока у вас нет пакетов", show_alert=True)


@dp.callback_query_handler(lambda callback:callback.data.startswith("package_"), state=States.main_menu)
async def show_package_info(callback_query: types.CallbackQuery):
    await callback_query.answer()
    package_id = callback_query.data.split("_")[-1]
    text = create_text(package_id)
    await bot.send_message(callback_query.from_user.id,text,reply_markup=package_kb(package_id), parse_mode="HTML",disable_web_page_preview=True)

@dp.callback_query_handler(lambda callback:callback.data.startswith("set_cost_package"), state=States.main_menu)
async def ask_package_cost(callback_query: types.CallbackQuery, state):
    await callback_query.answer()
    package_id = callback_query.data.split("_")[-1]
    await bot.send_message(
        callback_query.from_user.id,
        "Введите цену пакета"
    )
    await state.update_data(package_id=package_id)
    await States.waiting_for_package_cost.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=States.waiting_for_package_cost)
async def set_package_cost(message: types.Message, state):
    user_data = await state.get_data()
    try:
        package = Package.get_by_id(user_data["package_id"])
        package.cost = float(message.text)
        package.save()
        text = create_text(package.id)
        await message.answer(text,reply_markup=package_kb(package.id), parse_mode="HTML",disable_web_page_preview=True)
        await States.main_menu.set()
    except ValueError:
        await message.answer("Допускаются только цифры")

@dp.callback_query_handler(lambda callback:callback.data.startswith("add_to_package"), state=States.main_menu)
async def add_instructions(callback_query: types.CallbackQuery,state):
    await callback_query.answer()
    package_id = callback_query.data.split("_")[-1]
    await state.update_data(package_id=package_id,adding=True)
    await bot.send_message(
        callback_query.from_user.id,
        "Выберите продукты через поиск или закончите добавление",
        reply_markup=adding_kb(package_id)
    )
    await States.adding_products_to_package.set()


@dp.message_handler(lambda message:message.text.isdigit(),state=States.adding_products_to_package)
async def add_product(message: types.Message,state):
    user_data = await state.get_data()
    package = Package.get_or_none(Package.id == user_data["package_id"])
    if package is not None:
        product = Post.get_by_id(message.text)
        ProductsInPackage.create(
            package = package,
            product = product
        )
        text = create_text(package.id)
        await message.answer(text,reply_markup=adding_kb(package.id), parse_mode="HTML",disable_web_page_preview=True)
    else:
        await message.answer("Пакет не найден")


@dp.callback_query_handler(lambda callback:callback.data.startswith("end_adding_"), state=States.adding_products_to_package)
async def stop_adding(callback_query: types.CallbackQuery,state):
    package_id = callback_query.data.split("_")[-1]
    await States.main_menu.set()
    text = create_text(package_id)
    await bot.send_message(
        callback_query.from_user.id,
        text,
        reply_markup=package_kb(package_id),
        parse_mode="HTML",disable_web_page_preview=True
        )
    await state.update_data(adding=False)
    await callback_query.answer()
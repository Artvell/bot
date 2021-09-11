
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    """класс с состояниями бота"""
    main_menu = State()
    waiting_for_subcategory = State()
    subcategories = State()
    waiting_for_cost = State()
    searching = State()
    waiting_for_order_type = State()
    orders_list = State()
    order_info = State()
    waiting_for_link = State()
    waiting_for_driver_phone = State()
    waiting_for_delete_driver = State()
    waiting_for_spam = State()
    waiting_for_package_title = State()
    waiting_for_package_cost = State()
    adding_products_to_package = State()

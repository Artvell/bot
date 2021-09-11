
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    """класс с состояниями бота"""
    waiting_for_number = State()
    main_menu = State()
    waiting_for_subcategory = State()
    subcategories = State()
    waiting_for_order_type = State()
    orders_list = State()
    order_info = State()
    settings = State()
    settings_phone = State()
    settings_name = State()
    settings_delete_location = State()
    settings_add_location = State()
    settings_set_location_name = State()
    waiting_for_type = State()
    waiting_for_location = State()
    waiting_for_time = State()
    waiting_for_money_type = State()
    select_system_type = State()
    select_payment_type = State()
    waiting_for_approve = State()
    create_order = State()
    searching = State()
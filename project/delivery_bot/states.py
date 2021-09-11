from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    """класс с состояниями бота"""
    main_menu = State()
    waiting_for_phone = State()
    waiting_for_password = State()
    list_of_orders = State()
    order_info = State()
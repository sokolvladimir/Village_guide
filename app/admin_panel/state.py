from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMAdminPanel(StatesGroup):
    start_admin_panel = State()


class FSMAdminSettings(StatesGroup):
    add_admin_settings = State()
    remove_admin = State()
    add_admin = State()


class FSMService(StatesGroup):
    city = State()
    add_new_city = State()
    remove_city = State()

    services = State()
    add_new_service = State()
    remove_service = State()

    type_service = State()
    add_new_type_service = State()
    remove_type_service = State()


class FSMCards(StatesGroup):
    start_menu = State()
    add_cards = State()
    remove_cards = State()

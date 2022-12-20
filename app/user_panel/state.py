from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMUserPanel(StatesGroup):
    # State for user panel
    city_service = State()
    service_type_service = State()
    type_service_cards = State()
    show_card = State()
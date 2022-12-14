from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMAdminPanel(StatesGroup):
    start_admin_panel = State()
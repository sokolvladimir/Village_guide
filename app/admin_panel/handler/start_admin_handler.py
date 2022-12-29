from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.admin_panel.admin_text import start_admin_panel_text
from app.admin_panel.handler.services_handler import register_service_handler
from app.admin_panel.handler.admin_settings_handler import register_admin_settings
from app.admin_panel.keyboards import start_admin_kb, admin_settings_kb, city_kb
from app.admin_panel.methods import checking_for_administrator
from app.admin_panel.state import FSMAdminPanel, FSMAdminSettings, FSMService


async def start(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    async with state.proxy() as data:
        data['message'] = message
    user_name = message.from_user.username
    user_id = message.from_user.id
    is_admin = checking_for_administrator(user_id, user_name)
    async with state.proxy() as data:
        data['admin'] = is_admin
    match is_admin:
        case 0:
            await message.answer("Вы не являетесь администратором\n"
                                 "Для того, чтобы стать администратором, обратитесь к суперадминистратору")
        case 1:
            await message.answer(start_admin_panel_text, reply_markup=start_admin_kb(admin='Админ'))
            await FSMAdminPanel.start_admin_panel.set()
        case 2:
            await message.answer(start_admin_panel_text, reply_markup=start_admin_kb(admin='Супер Админ'))
            await FSMAdminPanel.start_admin_panel.set()
        case _:
            await message.answer("Произошла ошибка, попробуйте позже")


async def start_admin_panel(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["city_index"] = 1
    match call.data:
        case "add_cards":
            await call.message.edit_text("Выберите город или другое действие",
                                         reply_markup=city_kb(index=data["city_index"]))
            await FSMService.city.set()
        case "admin_panel":
            await call.message.edit_text("Выберите действие", reply_markup=admin_settings_kb)
            await FSMAdminSettings.add_admin_settings.set()
        case _:
            await state.finish()


def register_admin_panel(dp):
    dp.register_message_handler(start, commands=['admin_panel'], state='*')
    dp.register_callback_query_handler(start_admin_panel, state=FSMAdminPanel.start_admin_panel)
    register_admin_settings(dp)
    register_service_handler(dp)

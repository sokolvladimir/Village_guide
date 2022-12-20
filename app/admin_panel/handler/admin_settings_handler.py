from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Database.methods.admin_methods import delete_admin_by_username, add_new_admin
from app.admin_panel.admin_text import start_admin_panel_text
from app.admin_panel.keyboards import start_admin_kb, get_all_admins_kb, admin_settings_kb
from app.admin_panel.state import FSMAdminPanel, FSMAdminSettings


async def add_admin_settings(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        admin = data['admin']
    match call.data:
        case "add_admin":
            await call.message.edit_text("Введите никнейм администратора через\n"
                                         "Например: admin\n"
                                         "Или нажмите /break, чтобы вернуться назад")
            await FSMAdminSettings.add_admin.set()
        case "remove_admin":
            kb = get_all_admins_kb()
            if not kb:
                await call.message.edit_text("⚠️Администраторы отсутствуют\n\nВыберите другое действие",
                                             reply_markup=admin_settings_kb)
            else:
                await call.message.edit_text("Выберите администратора, которого хотите удалить", reply_markup=kb)
                await FSMAdminSettings.remove_admin.set()
        case "back":
            await call.message.edit_text(start_admin_panel_text,
                                         reply_markup=start_admin_kb(admin='Супер Админ' if admin == 2 else 'Админ'))
            await FSMAdminPanel.start_admin_panel.set()
        case _:
            await state.finish()


async def remove_admin(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await call.message.edit_text("Выберите действие", reply_markup=admin_settings_kb)
        await FSMAdminSettings.add_admin_settings.set()
    else:
        delete_admin_by_username(call.data)
        kb = get_all_admins_kb()
        if not kb:
            await call.message.edit_text("♻️ Администратор удален\n"
                                         "⚠️Администраторы отсутствуют\n\n"
                                         "Выберите действие", reply_markup=admin_settings_kb)
            await FSMAdminSettings.add_admin_settings.set()
        else:
            await call.message.edit_text("♻️ Администратор удален\n"
                                         "Выберите администратора, которого хотите удалить", reply_markup=kb)


async def add_admin(message: Message, state: FSMContext):
    if message.text == '/break':
        await message.answer("Выберите действие", reply_markup=admin_settings_kb)
        await FSMAdminSettings.add_admin_settings.set()
    else:
        add_new_admin(user_name=message.text)
        await message.answer("🟢️ Администратор добавлен\n"
                             "Выберите действие", reply_markup=admin_settings_kb)
        await FSMAdminSettings.add_admin_settings.set()


def register_admin_settings(dp):
    dp.register_callback_query_handler(add_admin_settings, state=FSMAdminSettings.add_admin_settings)
    dp.register_callback_query_handler(remove_admin, state=FSMAdminSettings.remove_admin)
    dp.register_message_handler(add_admin, state=FSMAdminSettings.add_admin)

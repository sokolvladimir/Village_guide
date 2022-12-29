from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.Database.methods.city_methods import add_new_city_in_db, delete_city_from_db
from app.Database.methods.services_method import add_new_service_in_db, delete_service_from_db
from app.Database.methods.type_service_method import add_new_type_service_in_db, delete_type_service_from_db
from app.admin_panel.admin_text import start_admin_panel_text
from app.admin_panel.handler.add_card_handler import register_add_card_handlers
from app.admin_panel.keyboards import start_admin_kb, back_kb, city_kb, city_remove_kb, get_services_kb, \
    remove_services_kb, get_type_service_kb, remove_type_services_kb, start_menu_add_card_kb
from app.admin_panel.state import FSMAdminPanel, FSMService, FSMCards


async def city(call: CallbackQuery, state: FSMContext):
    """Метод получает все города"""
    async with state.proxy() as data:
        admin = data['admin']
        if call.data.isdigit():
            data['city_id'] = int(call.data)
            data["service_index"] = 1
            await call.message.edit_text("Выберите нужный сервис",
                                         reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()
        match call.data:
            case "back":
                await call.message.edit_text(start_admin_panel_text,
                                             reply_markup=start_admin_kb(
                                                 admin='Супер Админ' if admin == 2 else 'Админ'))
                await FSMAdminPanel.start_admin_panel.set()
            case "_add":
                msg = await call.message.edit_text("Введите название города", reply_markup=back_kb)
                async with state.proxy() as data:
                    data['msg'] = msg
                await FSMService.add_new_city.set()
            case "_del":
                data["city_remove_index"] = 1
                await call.message.edit_text("Выберите город для удаления или другое действие",
                                             reply_markup=city_remove_kb(index=data["city_remove_index"]))
                await FSMService.remove_city.set()
            case "next":
                data["city_index"] += 1
                await call.message.edit_text("Выберите город или другое действие",
                                             reply_markup=city_kb(index=data["city_index"]))
            case "prev":
                data["city_index"] -= 1
                await call.message.edit_text("Выберите город или другое действие",
                                             reply_markup=city_kb(index=data["city_index"]))


async def add_new_city(message: Message | CallbackQuery, state: FSMContext):
    """Метод добавляет новый город"""
    async with state.proxy() as data:
        data["city_index"] = 1
        if isinstance(message, CallbackQuery):
            await message.message.edit_text("Выберите город или другое действие",
                                            reply_markup=city_kb(index=data["city_index"]))
            await FSMService.city.set()
        else:
            add_new_city_in_db(city_name=message.text)
            await message.answer("🟢 Город добавлен\n"
                                 "Выберите город или другое действие", reply_markup=city_kb(index=data["city_index"]))
            msg = data['msg']
            await msg.delete()
            await FSMService.city.set()


async def remove_city(call: CallbackQuery, state: FSMContext):
    """Метод удаляет город"""
    async with state.proxy() as data:
        if call.data.isdigit():
            delete_city_from_db(city_id=int(call.data))
            data["city_index"] = 1
            await call.message.edit_text("🟢 Город успешно удален\n"
                                         "Выберите город или другое действие", reply_markup=city_kb(data["city_index"]))
            await FSMService.city.set()
        elif call.data == "back":
            await call.message.edit_text("Выберите город или другое действие", reply_markup=city_kb(data["city_index"]))
            await FSMService.city.set()
        elif call.data == "next":
            data["city_remove_index"] += 1
            await call.message.edit_text("Выберите город для удаления или другое действие",
                                         reply_markup=city_remove_kb(index=data["city_remove_index"]))
        elif call.data == "prev":
            data["city_remove_index"] -= 1
            await call.message.edit_text("Выберите город для удаления или другое действие",
                                         reply_markup=city_remove_kb(index=data["city_remove_index"]))


async def services(call: CallbackQuery, state: FSMContext):
    """Метод открывает панель сервисов"""
    async with state.proxy() as data:
        if call.data.isdigit():
            data['service_id'] = int(call.data)
            data["type_service_index"] = 1
            await call.message.edit_text("Выберите тип услуги",
                                         reply_markup=get_type_service_kb(service_id=data['service_id'], index=1))
            await FSMService.type_service.set()

        elif call.data == "back":
            await call.message.edit_text("Выберите город или другое действие",
                                         reply_markup=city_kb(index=data["city_index"]))
            await FSMService.city.set()
        elif call.data == "_add":
            await call.message.edit_text("Введите название нового сервиса", reply_markup=back_kb)
            await FSMService.add_new_service.set()
        elif call.data == "_del":
            data["service_remove_index"] = 1
            await call.message.edit_text("Выберите сервис для удаления", reply_markup=remove_services_kb(index=1))
            await FSMService.remove_service.set()
        elif call.data == "next":
            data["service_index"] += 1
            await call.message.edit_text("Выберите сервис или другое действие",
                                         reply_markup=get_services_kb(index=data["service_index"]))
        elif call.data == "prev":
            data["service_index"] -= 1
            await call.message.edit_text("Выберите сервис или другое действие",
                                         reply_markup=get_services_kb(index=data["service_index"]))


async def add_new_service(message: Message | CallbackQuery, state: FSMContext):
    """Метод добавляет новый сервис"""
    async with state.proxy() as data:
        if isinstance(message, CallbackQuery):
            await message.message.edit_text("Выберите нужный сервис",
                                            reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()
        else:
            add_new_service_in_db(service_name=message.text)
            data["service_index"] = 1
            await message.answer("🟢 Сервис добавлен\n"
                                 "Выберите нужный сервис", reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()


async def remove_service(call: CallbackQuery, state: FSMContext):
    """Метод удаляет сервис"""
    async with state.proxy() as data:
        if call.data.isdigit():
            delete_service_from_db(service_id=int(call.data))
            data["service_index"] = 1
            await call.message.edit_text("🟢 Сервис успешно удален\n"
                                         "Выберите нужный сервис",
                                         reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()
        elif call.data == "back":
            await call.message.edit_text("Выберите нужный сервис",
                                         reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()
        elif call.data == "next":
            data["service_remove_index"] += 1
            await call.message.edit_text("Выберите сервис для удаления",
                                         reply_markup=remove_services_kb(index=data["service_remove_index"]))
        elif call.data == "prev":
            data["service_remove_index"] -= 1
            await call.message.edit_text("Выберите сервис для удаления",
                                         reply_markup=remove_services_kb(index=data["service_remove_index"]))


async def type_service(call: CallbackQuery, state: FSMContext):
    """Метод открывает панель типов сервисов"""
    async with state.proxy() as data:
        service_id = data['service_id']
        if call.data.isdigit():
            data['type_service_id'] = int(call.data)
            await call.message.edit_text("Выберите нужный функцонал", reply_markup=start_menu_add_card_kb)
            await FSMCards.start_menu.set()

        elif call.data == "back":
            data["service_index"] = 1
            await call.message.edit_text("Выберите нужный сервис",
                                         reply_markup=get_services_kb(index=data["service_index"]))
            await FSMService.services.set()
        elif call.data == "_add":
            await call.message.edit_text("Введите название нового типа сервиса", reply_markup=back_kb)
            await FSMService.add_new_type_service.set()
        elif call.data == "_del":
            data["type_service_remove_index"] = 1
            await call.message.edit_text("Выберите тип сервиса для удаления",
                                         reply_markup=remove_type_services_kb(service_id=service_id, index=1))
            await FSMService.remove_type_service.set()
        elif call.data == "next":
            data["type_service_index"] += 1
            await call.message.edit_text("Выберите тип сервиса",
                                         reply_markup=get_type_service_kb(service_id=service_id,
                                                                          index=data["type_service_index"]))
        elif call.data == "prev":
            data["type_service_index"] -= 1
            await call.message.edit_text("Выберите тип сервиса",
                                         reply_markup=get_type_service_kb(service_id=service_id,
                                                                          index=data["type_service_index"]))


async def add_new_type_service(message: Message | CallbackQuery, state: FSMContext):
    """Метод добавляет новый тип сервиса"""
    async with state.proxy() as data:
        service_id = data['service_id']
        if isinstance(message, CallbackQuery):
            data["type_service_index"] = 1
            await message.message.edit_text("Выберите тип услуги",
                                            reply_markup=get_type_service_kb(service_id=service_id, index=1))
            await FSMService.type_service.set()
        else:
            add_new_type_service_in_db(type_service_name=message.text, service_id=service_id)
            data["type_service_index"] = 1
            await message.answer("🟢 Тип сервиса добавлен\n"
                                 "Выберите тип услуги",
                                 reply_markup=get_type_service_kb(service_id=service_id, index=1))
            await FSMService.type_service.set()


async def remove_type_service(call: CallbackQuery, state: FSMContext):
    """Метод удаляет тип сервиса"""
    async with state.proxy() as data:
        service_id = data['service_id']
    if call.data.isdigit():
        delete_type_service_from_db(type_service_id=int(call.data))
        await call.message.edit_text("🟢 Тип сервиса успешно удален\n"
                                     "Выберите тип услуги", reply_markup=get_type_service_kb(service_id=service_id))
        await FSMService.type_service.set()
    elif call.data == "back":
        await call.message.edit_text("Выберите тип услуги", reply_markup=get_type_service_kb(service_id=service_id))
        await FSMService.type_service.set()
    elif call.data == "next":
        data["type_service_remove_index"] += 1
        await call.message.edit_text("Выберите тип сервиса для удаления",
                                     reply_markup=remove_type_services_kb(service_id=service_id,
                                                                          index=data["type_service_remove_index"]))
    elif call.data == "prev":
        data["type_service_remove_index"] -= 1
        await call.message.edit_text("Выберите тип сервиса для удаления",
                                     reply_markup=remove_type_services_kb(service_id=service_id,
                                                                          index=data["type_service_remove_index"]))


def register_service_handler(dp):
    dp.register_callback_query_handler(city, state=FSMService.city)
    dp.register_message_handler(add_new_city, state=FSMService.add_new_city)
    dp.register_callback_query_handler(remove_city, state=FSMService.remove_city)
    dp.register_callback_query_handler(services, state=FSMService.services)
    dp.register_message_handler(add_new_service, state=FSMService.add_new_service)
    dp.register_callback_query_handler(remove_service, state=FSMService.remove_service)
    dp.register_callback_query_handler(type_service, state=FSMService.type_service)
    dp.register_message_handler(add_new_type_service, state=FSMService.add_new_type_service)
    dp.register_callback_query_handler(remove_type_service, state=FSMService.remove_type_service)
    register_add_card_handlers(dp)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.Database.methods.admin_methods import get_all_simple_admins
from app.Database.methods.city_methods import get_cities
from app.Database.methods.services_method import get_all_services
from app.Database.methods.type_service_method import get_type_services

back = InlineKeyboardButton(text="Назад", callback_data="back")
add_button = InlineKeyboardButton(text="🟢 Добавить", callback_data="_add")
del_button = InlineKeyboardButton(text="🔴 Удалить", callback_data="_del")
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
cancel_kb = InlineKeyboardMarkup().add(cancel_button)
back_kb = InlineKeyboardMarkup().add(back)


def start_admin_kb(admin: str) -> InlineKeyboardMarkup:
    """Метод создает клавиатуру для администратора"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавление карточек", callback_data="add_cards")
        ],
    ])

    if admin == 'Супер Админ':
        keyboard.add(InlineKeyboardButton(text="Добавление администратора", callback_data="admin_panel"))
    return keyboard


admin_settings_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin")
    ],
    [
        InlineKeyboardButton(text="Удалить администратора", callback_data="remove_admin")
    ]
])

admin_settings_kb.add(back)


def city_kb():
    """Метод создает клавиатуру для выбора города"""
    cities = get_cities()
    keyboard = InlineKeyboardMarkup()
    for city in cities:
        city_name = city.get("city_name")
        city_id = city.get("city_id")
        keyboard.add(InlineKeyboardButton(text=city_name, callback_data=f"{city_id}"))

    keyboard.add(add_button, del_button)
    keyboard.add(back)
    return keyboard


def city_remove_kb():
    """Метод создает клавиатуру для удаления города"""
    cities = get_cities()
    keyboard = InlineKeyboardMarkup()
    for city in cities:
        city_name = city.get("city_name")
        city_id = city.get("city_id")
        keyboard.add(InlineKeyboardButton(text=city_name, callback_data=f"{city_id}"))
    keyboard.add(back)
    return keyboard


def get_all_admins_kb():
    """Метод создает клавиатуру для выбора администратора"""
    all_admins = get_all_simple_admins()
    keyboard = InlineKeyboardMarkup()
    if not all_admins:
        return None
    for admin in all_admins:
        user_name = admin.get("telegram_username")
        keyboard.add(InlineKeyboardButton(text=user_name, callback_data=f"{user_name}"))
    keyboard.add(back)
    return keyboard


def get_services_kb():
    """Метод создает клавиатуру для добавления услуг"""
    keyboard = InlineKeyboardMarkup()
    services = get_all_services()
    for service in services:
        service_name = service.get("service_name")
        service_id = service.get("service_id")
        keyboard.add(InlineKeyboardButton(text=service_name, callback_data=f"{service_id}"))
    keyboard.add(add_button, del_button)
    keyboard.add(back)
    return keyboard


def remove_services_kb():
    """Метод создает клавиатуру для удаления услуг"""
    keyboard = InlineKeyboardMarkup()
    services = get_all_services()
    for service in services:
        service_name = service.get("service_name")
        service_id = service.get("service_id")
        keyboard.add(InlineKeyboardButton(text=service_name, callback_data=f"{service_id}"))
    keyboard.add(back)
    return keyboard


def get_type_service_kb(service_id: int):
    """Метод создает клавиатуру для выбора типа услуги"""
    keyboard = InlineKeyboardMarkup()
    type_services = get_type_services(service_id)
    for type_service in type_services:
        type_service_name = type_service.get("type_service_name")
        type_service_id = type_service.get("type_service_id")
        keyboard.add(InlineKeyboardButton(text=type_service_name, callback_data=f"{type_service_id}"))
    keyboard.add(add_button, del_button)
    keyboard.add(back)
    return keyboard


def remove_type_services_kb(service_id: int):
    """Метод создает клавиатуру для удаления типа услуги"""
    keyboard = InlineKeyboardMarkup()
    type_services = get_type_services(service_id)
    for type_service in type_services:
        type_service_name = type_service.get("type_service_name")
        type_service_id = type_service.get("type_service_id")
        keyboard.add(InlineKeyboardButton(text=type_service_name, callback_data=f"{type_service_id}"))
    keyboard.add(back)
    return keyboard


def remove_card_kb(index: int, count_cards: int):
    """Метод создает клавиатуру для удаления карточки"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔴 Удалить", callback_data=f"remove_card_{index}"))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"prev_card"),
                 InlineKeyboardButton(text=f"{index + 1}/{count_cards}", callback_data="none"),
                 InlineKeyboardButton(text="▶️", callback_data=f"next_card"))
    keyboard.add(back)
    return keyboard


start_menu_add_card_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить карточку", callback_data="add_card")
    ],
    [
        InlineKeyboardButton(text="Удалить карточку", callback_data="remove_card")
    ]
])
start_menu_add_card_kb.add(back)


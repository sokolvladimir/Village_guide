from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.Database.methods.city_methods import get_cities
from app.Database.methods.services_method import get_services_for_city
from app.Database.methods.type_service_method import get_type_service_for_city
from app.admin_panel.keyboards import back


def get_cities_kb():
    """Метод создает клавиатуру для выбора города"""
    cities = get_cities()
    keyboard = InlineKeyboardMarkup()
    for city in cities:
        city_name = city.get("city_name")
        city_id = city.get("city_id")
        keyboard.add(InlineKeyboardButton(text=city_name, callback_data=f"{city_id}"))
    return keyboard


def get_services_kb(city_id: int):
    """Метод создает клавиатуру для выбора услуги"""
    services = get_services_for_city(city_id)
    keyboard = InlineKeyboardMarkup()
    for service in services:
        service_name = service.get("service_name")
        service_id = service.get("service_id")
        keyboard.add(InlineKeyboardButton(text=service_name, callback_data=f"{service_id}"))
    keyboard.add(back)
    return keyboard


def get_type_services_kb(service_id: int, city_id: int):
    """Метод создает клавиатуру для выбора типа услуги"""
    keyboard = InlineKeyboardMarkup()
    list_type_services = get_type_service_for_city(city_id, service_id)
    for type_service in list_type_services:
        type_service_name = type_service.get("type_service_name")
        type_service_id = type_service.get("type_service_id")
        keyboard.add(InlineKeyboardButton(text=type_service_name, callback_data=f"{type_service_id}"))
    keyboard.add(back)
    return keyboard



def show_card_kb(index: int, count_cards: int, card_link: str):
    """Метод создает клавиатуру для удаления карточки"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="📡 Ссылка", url=card_link))
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"prev_card"),
                 InlineKeyboardButton(text=f"{index + 1}/{count_cards}", callback_data="none"),
                 InlineKeyboardButton(text="▶️", callback_data=f"next_card"))
    keyboard.add(back)
    return keyboard

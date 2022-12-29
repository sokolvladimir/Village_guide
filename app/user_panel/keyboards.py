from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.Database.methods.city_methods import get_city_with_card
from app.Database.methods.services_method import get_services_for_city
from app.Database.methods.type_service_method import get_type_service_for_city


back = InlineKeyboardButton(text="Назад", callback_data="back")
def next_buttons(list_buttons: list, index: int):
    """Метод добавляет кнопки для переключения"""
    count_buttons = 6
    if len(list_buttons) <= count_buttons:
        return {"list_buttons": list_buttons, "next_buttons": None}
    else:
        if len(list_buttons) % count_buttons > 0:
            counts = len(list_buttons) // count_buttons + 1
        else:
            counts = len(list_buttons) // count_buttons  # это целые части

        buttons = [InlineKeyboardButton(text="◀️", callback_data=f"prev"),
                   InlineKeyboardButton(text=f"{index}/{counts}", callback_data="none"),
                   InlineKeyboardButton(text="▶️", callback_data=f"next")]

        if index == counts:
            buttons[2] = InlineKeyboardButton(text=" ", callback_data=f"none")
        elif index == 1:
            buttons[0] = InlineKeyboardButton(text=" ", callback_data=f"none")

        if index == counts:
            list_buttons = list_buttons[(index - 1) * count_buttons:]
        else:
            list_buttons = list_buttons[(index - 1) * count_buttons:index * count_buttons]

        return {"list_buttons": list_buttons, "next_buttons": buttons}


def get_cities_kb(index: int):
    """Метод создает клавиатуру для выбора города"""
    cities = get_city_with_card()
    dct = next_buttons(cities, index)
    keyboard = InlineKeyboardMarkup()
    for city in dct["list_buttons"]:
        city_name = city.get("city_name")
        city_id = city.get("city_id")
        keyboard.add(InlineKeyboardButton(text=city_name, callback_data=f"{city_id}"))
    if dct["next_buttons"]:
        keyboard.row(*dct["next_buttons"])
    return keyboard


def get_services_kb(city_id: int, index: int):
    """Метод создает клавиатуру для выбора услуги"""
    services = get_services_for_city(city_id)
    dct = next_buttons(services, index)
    keyboard = InlineKeyboardMarkup()
    for service in dct["list_buttons"]:
        service_name = service.get("service_name")
        service_id = service.get("service_id")
        keyboard.add(InlineKeyboardButton(text=service_name, callback_data=f"{service_id}"))
    if dct["next_buttons"]:
        keyboard.row(*dct["next_buttons"])
    keyboard.add(back)
    return keyboard


def get_type_services_kb(service_id: int, city_id: int, index: int):
    """Метод создает клавиатуру для выбора типа услуги"""
    keyboard = InlineKeyboardMarkup()
    list_type_services = get_type_service_for_city(city_id, service_id)
    dct = next_buttons(list_type_services, index)
    for type_service in dct["list_buttons"]:
        type_service_name = type_service.get("type_service_name")
        type_service_id = type_service.get("type_service_id")
        keyboard.add(InlineKeyboardButton(text=type_service_name, callback_data=f"{type_service_id}"))
    if dct["next_buttons"]:
        keyboard.row(*dct["next_buttons"])
    keyboard.add(back)
    return keyboard


def show_card_kb(index: int, count_cards: int, card_link: str):
    """Метод создает клавиатуру для удаления карточки"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="📡 Ссылка", url=card_link))
    keyboard = add_buttons_prev_next(index + 1, count_cards, keyboard)
    keyboard.add(back)
    return keyboard


def add_buttons_prev_next(index: int, counts: int, keyboard: InlineKeyboardMarkup):
    """Метод добавляет кнопки для переключения"""
    keyboard.add(InlineKeyboardButton(text="◀️", callback_data=f"prev"),
                 InlineKeyboardButton(text=f"{index}/{counts}", callback_data="none"),
                 InlineKeyboardButton(text="▶️", callback_data=f"next"))
    return keyboard

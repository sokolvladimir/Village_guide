from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto

from app.Database.methods.card_method import get_cards
from app.user_panel.keyboards import get_cities_kb, get_services_kb, show_card_kb, get_type_services_kb
from app.user_panel.state import FSMUserPanel


async def start_user_panel(message: types.Message):
    """Метод для старта панели пользователя"""
    await message.answer("Выберите Город", reply_markup=get_cities_kb())
    await FSMUserPanel.city_service.set()


async def city_services(call: types.CallbackQuery, state: FSMContext):
    """Метод для получения всех сервисов в городе"""
    async with state.proxy() as data:
        data['city_id'] = int(call.data)
        data["next_index"] = 2
        await call.message.edit_text("Выберите нужный сервис", reply_markup=get_services_kb(int(call.data), data))
    await FSMUserPanel.service_type_service.set()


async def service_type_services(call: types.CallbackQuery, state: FSMContext):
    """Метод для получения всех услуг в городе"""
    async with state.proxy() as data:
        match call.data:
            case "back":
                await call.message.edit_text("Выберите Город", reply_markup=get_cities_kb())
                await FSMUserPanel.city_service.set()
            case "next":
                data["next_index"] += 2
                await call.message.edit_text("Выберите нужный сервис", reply_markup=get_services_kb(data['city_id'], data))
            case "prev":
                data["next_index"] -= 2
                await call.message.edit_text("Выберите нужный сервис", reply_markup=get_services_kb(data['city_id'], data))
            case _:
                async with state.proxy() as data:
                    data['service_id'] = int(call.data)
                    city_id = data.get("city_id")
                    await call.message.edit_text("Выберите нужную услугу",
                                                 reply_markup=get_type_services_kb(data['service_id'], city_id))
                    await FSMUserPanel.type_service_cards.set()


async def type_service_cards(call: types.CallbackQuery, state: FSMContext):
    """Метод для получения всех типов услуг в городе"""
    async with state.proxy() as data:
        city_id = data["city_id"]
        service_id = data['service_id']
        next_index = data["next_index"]
        match call.data:
            case "back":
                await call.message.edit_text("Выберите нужный сервис", reply_markup=get_services_kb(city_id, next_index))
                await FSMUserPanel.service_type_service.set()
            case _:
                data["type_service_id"] = int(call.data)
                cards = get_cards(type_service_id=data["type_service_id"], village_id=data["city_id"])
                data["list_cards"] = cards
                data["index"] = 0
                data["count_cards"] = len(cards)
                if data["count_cards"]:
                    caption = f"{cards[0]['card_title']}\n{cards[0]['card_description']}"
                    if len(caption) > 1024:
                        caption = caption[:1021] + "..."
                    await call.message.answer_photo(cards[0]['card_image'], caption=caption,
                                                    reply_markup=show_card_kb(index=0, count_cards=data["count_cards"],
                                                                              card_link=cards[0]['site_link']))
                    await call.message.delete()
                    await FSMUserPanel.show_card.set()
                else:
                    await call.message.edit_text("Карточек нет\nВыберите нужную услугу",
                                                 reply_markup=get_type_services_kb(service_id, city_id))
                    await FSMUserPanel.type_service_cards.set()


async def show_card(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city_id = data["city_id"]
        service_id = data['service_id']
        match call.data:
            case "next":
                data["index"] += 1
                if data["index"] == data["count_cards"]:
                    data["index"] = 0
                card = data["list_cards"][data["index"]]
                caption = f"{card['card_title']}\n{card['card_description']}\n"
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                await call.message.edit_media(InputMediaPhoto(media=card['card_image'], caption=caption),
                                              reply_markup=show_card_kb(index=data["index"],
                                                                        count_cards=data["count_cards"],
                                                                        card_link=card['site_link']))
            case "prev":
                data["index"] -= 1
                if data["index"] == -1:
                    data["index"] = data["count_cards"] - 1
                card = data["list_cards"][data["index"]]
                caption = f"{card['card_title']}\n{card['card_description']}\n"
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                await call.message.edit_media(InputMediaPhoto(media=card['card_image'], caption=caption),
                                              reply_markup=show_card_kb(index=data["index"],
                                                                        count_cards=data["count_cards"],
                                                                        card_link=card['site_link']))
            case "none":
                pass
            case "back":
                await call.message.answer("Выберите нужный функцонал",
                                          reply_markup=get_type_services_kb(service_id , city_id))
                await call.message.delete()
                await FSMUserPanel.type_service_cards.set()


def register_user_panel_handler(dp: Dispatcher):
    dp.register_message_handler(start_user_panel, commands="start", state="*")
    dp.register_callback_query_handler(city_services, state=FSMUserPanel.city_service)
    dp.register_callback_query_handler(service_type_services, state=FSMUserPanel.service_type_service)
    dp.register_callback_query_handler(type_service_cards, state=FSMUserPanel.type_service_cards)
    dp.register_callback_query_handler(show_card, state=FSMUserPanel.show_card)


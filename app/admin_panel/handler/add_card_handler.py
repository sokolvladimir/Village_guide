from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto

from app.Database.methods.card_method import add_card_in_db, get_cards, remove_card_from_db
from app.admin_panel.keyboards import get_type_service_kb, cancel_kb, start_menu_add_card_kb, remove_card_kb
from app.admin_panel.state import FSMCards, FSMService


async def start_menu(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        service_id = data['service_id']
        match call.data:
            case "add_card":
                msg = await call.message.edit_text("Введите название карточки", reply_markup=cancel_kb)
                data['msg'] = msg
                await FSMCards.add_cards.set()
            case "remove_card":
                async with state.proxy() as data:
                    cards = get_cards(type_service_id=data['type_service_id'], village_id=data['city_id'])
                    data["list_cards"] = cards
                    data["index"] = 0
                    data["count_cards"] = len(cards)
                    if data["count_cards"]:
                        caption = f"{cards[0]['card_title']}\n{cards[0]['card_description']}\n{cards[0]['site_link']}"
                        if len(caption) > 1024:
                            caption = caption[:1021] + "..."
                        await call.message.answer_photo(cards[0]['card_image'], caption=caption,
                                                        reply_markup=remove_card_kb(index=0,
                                                                                    count_cards=data["count_cards"]))
                        await call.message.delete()
                        await FSMCards.remove_cards.set()

                    else:
                        await call.message.edit_text("Карточек нет", reply_markup=start_menu_add_card_kb)
                        await FSMCards.start_menu.set()

            case "back":
                await call.message.edit_text("Выберите тип услуги",
                                             reply_markup=get_type_service_kb(service_id=service_id))
                await FSMService.type_service.set()


async def add_card(message: Message | CallbackQuery, state: FSMContext):
    """Метод добавляет карточку"""
    async with state.proxy() as data:
        if isinstance(message, CallbackQuery):
            await message.message.edit_text("Выберите нужный функцонал", reply_markup=start_menu_add_card_kb)
            data["card_title"] = ""
            data["card_description"] = ""
            data["card_link"] = ""
            data["card_photo"] = ""
            await FSMCards.start_menu.set()
        else:
            if not data.get("card_title"):
                data["card_title"] = message.text
                msg = await message.answer("Введите описание карточки", reply_markup=cancel_kb)
                await data['msg'].delete()
                data['msg'] = msg
            elif not data.get("card_description"):
                data["card_description"] = message.text
                msg = await message.answer("Укажите ссылку на карточку", reply_markup=cancel_kb)
                await data['msg'].delete()
                data['msg'] = msg
            elif not data.get("card_link"):
                data["card_link"] = message.text
                msg = await message.answer("Отправьте фото карточки", reply_markup=cancel_kb)
                await data['msg'].delete()
                data['msg'] = msg
            elif not data.get("card_photo"):
                if message.content_type == "photo":
                    data["card_photo"] = message.photo[0].file_id
                    await message.answer("🟢 Карточка добавлена", reply_markup=start_menu_add_card_kb)
                    add_card_in_db(card_title=data["card_title"],
                                   card_description=data["card_description"],
                                   card_image=data["card_photo"],
                                   site_link=data["card_link"],
                                   type_service_id=data['type_service_id'],
                                   village_id=data['city_id'])
                    data["card_title"] = ""
                    data["card_description"] = ""
                    data["card_link"] = ""
                    data["card_photo"] = ""
                    await data['msg'].delete()
                    data['msg'] = None
                    await FSMCards.start_menu.set()


async def remove_card(call: CallbackQuery, state: FSMContext):
    # достать карточки для этого города и этой услуги
    async with state.proxy() as data:
        match call.data.split("_"):
            case ("remove", "card", index):
                card = data["list_cards"].pop(int(index))
                card_id = card["card_id"]
                data["count_cards"] -= 1
                remove_card_from_db(card_id=card_id)
                if not data["count_cards"]:
                    await call.message.answer("🟢 Карточка удалена\nВыберите нужный функцонал",
                                              reply_markup=start_menu_add_card_kb)
                    await call.message.delete()
                    await FSMCards.start_menu.set()
                    return
                if data["index"] == data["count_cards"]:
                    data["index"] -= 1

                card = data["list_cards"][data["index"]]
                caption = f"{card['card_title']}\n{card['card_description']}\n{card['site_link']}"
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                await call.message.edit_media(InputMediaPhoto(media=card['card_image'], caption=caption),
                                              reply_markup=remove_card_kb(index=data["index"],
                                                                          count_cards=data["count_cards"]))

            case ("next", "card"):
                data["index"] += 1
                if data["index"] == data["count_cards"]:
                    data["index"] = 0
                card = data["list_cards"][data["index"]]
                caption = f"{card['card_title']}\n{card['card_description']}\n{card['site_link']}"
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                await call.message.edit_media(InputMediaPhoto(media=card['card_image'], caption=caption),
                                              reply_markup=remove_card_kb(index=data["index"],
                                                                          count_cards=data["count_cards"]))
            case ("prev", "card"):
                data["index"] -= 1
                if data["index"] == -1:
                    data["index"] = data["count_cards"] - 1
                card = data["list_cards"][data["index"]]
                caption = f"{card['card_title']}\n{card['card_description']}\n{card['site_link']}"
                if len(caption) > 1024:
                    caption = caption[:1021] + "..."
                await call.message.edit_media(InputMediaPhoto(media=card['card_image'], caption=caption),
                                              reply_markup=remove_card_kb(index=data["index"],
                                                                          count_cards=data["count_cards"]))
            case ["none"]:
                pass
            case ["back"]:
                await call.message.answer("Выберите нужный функцонал", reply_markup=start_menu_add_card_kb)
                await call.message.delete()
                await FSMCards.start_menu.set()


def register_add_card_handlers(dp):
    dp.register_callback_query_handler(start_menu, state=FSMCards.start_menu)
    dp.register_message_handler(add_card, content_types=["text", "photo"], state=FSMCards.add_cards)
    dp.register_callback_query_handler(add_card, state=FSMCards.add_cards)
    dp.register_callback_query_handler(remove_card, state=FSMCards.remove_cards)

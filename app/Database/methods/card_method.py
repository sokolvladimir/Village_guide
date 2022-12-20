from app.Database.create_database import Card, Session


def add_card_in_db(card_title: str, card_description: str, card_image: str, site_link: str, type_service_id: int,
                   village_id: int):
    """Метод добавляет новую карточку"""
    with Session() as session:
        card = Card(title=card_title, description=card_description, site_link=site_link, picture_link=card_image,
                    type_service_id=type_service_id, village_id=village_id, active=True)
        session.add(card)
        session.commit()


def get_cards(type_service_id: int, village_id: int):
    """Метод получает карточки по типу услуги и поселку"""
    with Session() as session:
        cards = session.query(Card).filter(Card.type_service_id == type_service_id,
                                           Card.village_id == village_id).all()
        list_cards = []
        if cards:
            for card in cards:
                list_cards.append({"card_id": card.id, "card_title": card.title, "card_description": card.description,
                                   "card_image": card.picture_link, "site_link": card.site_link})
        return list_cards


def remove_card_from_db(card_id: int):
    """Метод удаляет карточку"""
    with Session() as session:
        session.query(Card).filter(Card.id == card_id).delete()
        session.commit()

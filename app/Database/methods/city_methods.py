from app.Database.create_database import Village, Session


def get_cities():
    """Метод получает все города"""
    with Session() as session:
        cities = session.query(Village).all()
        list_cities = []
        if cities:
            for city in cities:
                list_cities.append({"city_id": city.id, "city_name": city.name})
        return list_cities


def add_new_city_in_db(city_name: str):
    """Метод добавляет новый город"""
    with Session() as session:
        city = Village(name=city_name)
        session.add(city)
        session.commit()


def delete_city_from_db(city_id: int):
    """Метод удаляет город и все его карточки"""
    with Session() as session:
        session.query(Village).filter(Village.id == city_id).delete()
        session.commit()

from app.Database.create_database import Session, Services, TypeServices, Card


def get_all_services():
    """Метод получает все услуги"""
    with Session() as session:
        services = session.query(Services).all()
        list_services = []
        if services:
            for service in services:
                list_services.append({"service_id": service.id, "service_name": service.name})
        return list_services


def add_new_service_in_db(service_name: str):
    """Метод добавляет новую услугу"""
    with Session() as session:
        service = Services(name=service_name)
        session.add(service)
        session.commit()


def delete_service_from_db(service_id: int):
    """Метод удаляет услугу и все ее карточки"""
    with Session() as session:
        type_services = session.query(TypeServices).filter(TypeServices.services_id == service_id).all()
        if type_services:
            for type_service in type_services:
                session.query(TypeServices).filter(TypeServices.id == type_service.id).delete(synchronize_session='fetch')
        session.query(Services).filter(Services.id == service_id).delete()
        session.commit()


def get_services_for_city(city_id):
    """Метод получает все услуги по городу и проверяет есть ли карточки по этой услуге"""
    with Session() as session:
        services = session.query(Services).join(TypeServices).join(Card).filter(Card.village_id == city_id).all()
        list_services = []
        if services:
            for service in services:
                list_services.append({"service_id": service.id, "service_name": service.name})
        return list_services

from app.Database.create_database import Session, TypeServices, Services, Card


def get_type_services(service_id: int):
    """Метод получает все типы услуг по конкретной услуге"""
    with Session() as session:
        type_services = session.query(TypeServices).filter(TypeServices.services_id == service_id).all()
        list_type_services = []
        if type_services:
            for type_service in type_services:
                list_type_services.append({"type_service_id": type_service.id, "type_service_name": type_service.name})
        return list_type_services


def add_new_type_service_in_db(type_service_name: str, service_id: int):
    """Метод добавляет новый тип услуги"""
    with Session() as session:
        type_service = TypeServices(name=type_service_name, services_id=service_id)
        session.add(type_service)
        session.commit()


def delete_type_service_from_db(type_service_id: int):
    """Метод удаляет тип услуги"""
    with Session() as session:
        session.query(TypeServices).filter(TypeServices.id == type_service_id).delete()
        session.commit()


def get_type_service_for_city(city_id: int, service_id: int):
    """Метод получает все типы услуг по конкретной услуге и конкретному городу"""
    with Session() as session:
        type_services = session.query(TypeServices).join(Card).filter(Card.village_id == city_id,
                                                                      TypeServices.services_id == service_id).all()
        list_type_services = []
        if type_services:
            for type_service in type_services:
                list_type_services.append({"type_service_id": type_service.id, "type_service_name": type_service.name})
        return list_type_services

import logging

from app.Database.create_database import Session, Admin


def get_all_admins():
    try:
        with Session() as session:
            admins = session.query(Admin).all()
            admin_list = []
            for admin in admins:
                dct = {"telegram_username": admin.telegram_username,
                       "telegram_id": admin.telegram_id,
                       "status": admin.status}
                admin_list.append(dct)
            return admin_list
    except Exception as ex:
        logging.error(f"Error in get_all_admins: {ex}")
        return None


def get_all_simple_admins():
    try:
        with Session() as session:
            admins = session.query(Admin).filter(Admin.status == 'Админ').all()
            admin_list = []
            for admin in admins:
                dct = {"telegram_username": admin.telegram_username,
                       "telegram_id": admin.telegram_id,
                       "status": admin.status}
                admin_list.append(dct)
            return admin_list
    except Exception as ex:
        logging.error(f"Error in get_all_simple_admins: {ex}")
        return None


def add_new_name_for_admin(user_id: int, user_name: str):
    try:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.telegram_id == user_id).first()
            admin.telegram_username = user_name
            session.add(admin)
            session.commit()
    except Exception as ex:
        logging.error(f"Error in add_new_name_for_admin: {ex}")
        return None

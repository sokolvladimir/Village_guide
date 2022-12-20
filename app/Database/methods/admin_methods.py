import logging

from app.Database.create_database import Session, Admin


def add_first_admin(user_id: int, user_name: str):
    try:
        with Session() as session:
            admin = Admin(telegram_id=user_id, telegram_username=user_name, status='super_admin')
            session.add(admin)
            session.commit()
        return True
    except Exception as ex:
        logging.error(f"Error in add_first_admin: {ex}")
        return None


def add_new_admin(user_name: str):
    try:
        with Session() as session:
            admin = Admin(telegram_username=user_name, status='admin')
            session.add(admin)
            session.commit()
    except Exception as ex:
        logging.error(f"Error in add_new_admin: {ex}")
        return None


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
            admins = session.query(Admin).filter(Admin.status == 'admin').all()
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


def delete_admin_by_username(user_name: str):
    try:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.telegram_username == user_name).first()
            session.delete(admin)
            session.commit()
    except Exception as ex:
        logging.error(f"Error in delete_admin_by_username: {ex}")
        return None


def add_id_for_new_admin(user_name: str, user_id: int):
    try:
        with Session() as session:
            admin = session.query(Admin).filter(Admin.telegram_username == user_name).first()
            admin.telegram_id = user_id
            session.add(admin)
            session.commit()
    except Exception as ex:
        logging.error(f"Error in add_id_for_new_admin: {ex}")
        return None

from app.Database.create_database import AdminStatus
from app.Database.methods.admin_methods import get_all_admins, add_new_name_for_admin, add_first_admin, \
    add_id_for_new_admin


def checking_for_administrator(user_id: int, user_name: str) -> int:
    """Метод проверяет, является ли пользователь администратором
    0 - не администратор
    1 - администратор
    2 - суперадминистратор"""
    list_of_admins = get_all_admins()
    if list_of_admins is None:
        return 0
    elif not list_of_admins:
        if add_first_admin(user_id, user_name):
            return 2
        else:
            return 0
    for admin in list_of_admins:
        if admin['telegram_id'] == user_id:
            if admin["telegram_username"] != user_name:
                add_new_name_for_admin(user_id, user_name)
            if admin['status'] == AdminStatus.admin:
                return 1
            elif admin['status'] == AdminStatus.super_admin:
                return 2
        if not admin['telegram_id'] and admin['telegram_username'] == user_name:
            add_id_for_new_admin(user_name, user_id)
            return 1
    return 0

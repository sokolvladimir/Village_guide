from app.Database.methods.admin_methods import get_all_admins, add_new_name_for_admin


def checking_for_administrator(user_id: int, user_name: str) -> int:
    """Метод проверяет, является ли пользователь администратором
    0 - не администратор
    1 - администратор
    2 - суперадминистратор"""
    list_of_admins = get_all_admins()
    for admin in list_of_admins:
        if admin['telegram_id'] == user_id:
            if admin["username"] != user_name:
                add_new_name_for_admin(user_id, user_name)
            if admin['status'] == 'Админ':
                return 1
            elif admin['status'] == 'Супер Админ':
                return 2
    return 0

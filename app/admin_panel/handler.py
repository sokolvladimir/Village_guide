from aiogram import types

from app.admin_panel.admin_text import start_admin_panel_text
from app.admin_panel.methods import checking_for_administrator


async def start_admin_panel(message: types.Message):
    user_name = message.from_user.username
    user_id = message.from_user.id
    is_admin = checking_for_administrator(user_id, user_name)
    match is_admin:
        case 0:
            await message.answer("Вы не являетесь администратором\n"
                                 "Для того, чтобы стать администратором, обратитесь к суперадминистратору")
        case 1:
            await message.answer(start_admin_panel_text, reply_markup=None)
        case 2:
            await message.answer(start_admin_panel_text, reply_markup=None)
        case _:
            await message.answer("Произошла ошибка, попробуйте позже")


def register_admin_panel(dp):
    dp.register_message_handler(start_admin_panel, commands=['admin_panel'], state='*')
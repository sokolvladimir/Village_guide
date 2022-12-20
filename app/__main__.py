from aiogram import executor

from app.bot.bot_init import dp
from app.admin_panel.handler import start_admin_handler
from app.user_panel.handler import register_user_panel_handler

start_admin_handler.register_admin_panel(dp)
register_user_panel_handler(dp)


executor.start_polling(dp, skip_updates=True)

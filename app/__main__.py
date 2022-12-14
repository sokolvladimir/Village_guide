from aiogram import executor


from app.bot.bot_init import dp

executor.start_polling(dp, skip_updates=True)

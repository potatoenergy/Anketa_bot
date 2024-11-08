# Импортируем необходимые модули
import logging

from aiogram import Dispatcher
from config import ADMINS
from loader import bot


# Определяем функцию для отправки уведомления администраторам о запуске бота
async def on_startup_notify(dp: Dispatcher, bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "🆙 Бот запущен и готов")
        except Exception as err:
            logging.error(err)


# Определяем функцию для отправки уведомлений администраторам
async def notify_admins(message: str):
    for admin in ADMINS:
        await bot.send_message(admin, message)

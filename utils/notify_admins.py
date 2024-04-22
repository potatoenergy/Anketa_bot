import datetime
import logging
from aiogram import Dispatcher
from loader import bot
from data.config import ADMINS

date_time_now = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S').split(',')
date, time = 0, 1
date_now = date_time_now[date]
time_now = date_time_now[time].strip()

ON_STARTUP_PHRASE = f'''🟢 Система успешно запущена
📅 {date_now}
🕒 {time_now}
'''


async def on_startup_notify():
    for admin in ADMINS:
        try:
            await bot.send_message(admin, ON_STARTUP_PHRASE)

        except Exception as err:
            logging.exception(err)

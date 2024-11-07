# Импортируем необходимые модули
import asyncio
from aiogram import Dispatcher, Bot
from handlers import setup_message_routers
from loader import dp, bot, set_commands
from middlewares import ThrottlingMiddleware
from utils.notify import on_startup_notify
from database import create_tables

# Определяем основную функцию
async def main():
    # Настраиваем маршрутизацию сообщений
    await setup_message_routers()
    # Настраиваем middleware
    await _setup_middleware(dp)
    # Создаем таблицы в базе данных
    await _create_tables()
    # Устанавливаем команды бота
    await set_commands()
    # Отправляем уведомление о запуске администраторам
    await on_startup_notify(dp, bot)
    # Начинаем опрос обновлений
    await _start_polling(dp, bot)

# Определяем функцию для настройки middleware
async def _setup_middleware(dp: Dispatcher) -> None:
    dp.message.middleware(ThrottlingMiddleware())

# Определяем функцию для создания таблиц в базе данных
async def _create_tables() -> None:
    await create_tables()

# Определяем функцию для начала опроса обновлений
async def _start_polling(dp: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запускаем основную функцию, если этот скрипт запущен напрямую
if __name__ == '__main__':
    asyncio.run(main())
# Импортируем необходимые модули
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

# Создаем объект DefaultBotProperties для настройки бота
default_bot_properties = DefaultBotProperties(parse_mode='HTML')
# Создаем объект Bot с токеном бота и настройками
bot = Bot(token=BOT_TOKEN, properties=default_bot_properties)
# Создаем объект Dispatcher с ботом и хранилищем в памяти
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# Определяем функцию для установки команд бота
async def set_commands():
    commands = [
        {"command": "start", "description": "Заполнить/отредактировать анкету"},
    ]
    await bot.set_my_commands(commands)
# Импортируем необходимые модули
from loader import bot, dp


# Определяем функцию для настройки маршрутизации сообщений
async def setup_message_routers():
    # Импортируем обработчики сообщений из других модулей
    from . import cancel, menu, start

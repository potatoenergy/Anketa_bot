# Импортируем необходимые модули
from loader import dp, bot

# Определяем функцию для настройки маршрутизации сообщений
async def setup_message_routers():
    # Импортируем обработчики сообщений из других модулей
    from . import start
    from . import cancel
    from . import menu
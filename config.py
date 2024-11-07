# Импортируем необходимый модуль
from environs import Env

# Создаем объект Env для чтения переменных окружения
env = Env()
# Читаем переменные окружения из файла .env
env.read_env()

# Получаем токен бота из переменной окружения
BOT_TOKEN: str = env.str("BOT_TOKEN")
# Получаем список администраторов из переменной окружения
ADMINS: list[int] = env.list("ADMINS")
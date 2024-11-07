# Импортируем необходимый модуль
import logging

# Настраиваем логирование в файл logger.log
logging.basicConfig(filename='logger.log', encoding='utf-8', format="%(asctime)s %(levelname)s %(message)s", level=logging.ERROR)
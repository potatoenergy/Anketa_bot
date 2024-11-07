# Импортируем необходимые модули
from aiogram.fsm.state import StatesGroup, State

# Определяем группу состояний для функции "мегафона"
class MegaphoneStates(StatesGroup):
    # Состояние для выбора типа текста для отправки в мегафон
    text_type = State()
    # Состояние для выбора типа текста с картинкой для отправки в мегафон
    pic_text_type = State()
    # Состояние для выбора типа GIF для отправки в мегафон
    gif_text_type = State()
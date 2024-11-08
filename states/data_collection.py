# Импортируем необходимые модули
from aiogram.fsm.state import State, StatesGroup


# Определяем группу состояний для сбора данных пользователя
class Form(StatesGroup):
    # Состояние для вопроса о повторении заполнения анкеты
    repeat = State()
    # Состояние для вопроса о полном имени пользователя
    act_full_name = State()
    # Состояние для вопроса о городе пользователя
    act_city = State()
    # Состояние для вопроса о возрасте пользователя
    act_age = State()
    # Состояние для вопроса об опыте работы пользователя
    act_work_experience = State()
    # Состояние для вопроса об образовании пользователя
    act_education = State()
    # Состояние для вопроса о навыках пользователя
    act_skills = State()
    # Состояние для вопроса о способах связи
    act_contact = State()

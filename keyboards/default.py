# Импортируем необходимые модули
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Создаем клавиатуру с основными командами
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Заполнить анкету")]], resize_keyboard=True)

# Создаем клавиатуру с кнопкой для отправки геолокации
geo_button = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text="Отправить геолокацию", request_location=True)
]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True)

# Создаем клавиатуру для удаления клавиатуры у пользователя
remove_keyboard = ReplyKeyboardRemove()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заполнить анкету")
        ]
    ],
    resize_keyboard=True
)

geo_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить геолокацию", request_location=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

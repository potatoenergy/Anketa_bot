from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Press", callback_data="btn_press")
        ],
        [
            InlineKeyboardButton(text="Link", url="https://ya.ru")
        ]
    ],
)

# Импортируем необходимые модули
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создаем инлайн-клавиатуру с двумя кнопками
inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Press", callback_data="btn_press"),
    InlineKeyboardButton(text="Link", url="https://ya.ru")
]])

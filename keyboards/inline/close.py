from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder


close_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Закрыть", callback_data="cancel")
        ]
    ],
)

# close_inline_keyboard = InlineKeyboardBuilder()
# close_inline_keyboard.row(
#     InlineKeyboardButton(text='Закрыть', callback_data='cancel'),
#     width=1
# )

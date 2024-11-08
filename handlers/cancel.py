# Импортируем необходимые модули
import logging

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from loader import bot, dp


# Определяем обработчик для callback query с данными "cancel"
@dp.callback_query(F.data == "cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    try:
        # Удаляем сообщение с кнопкой "cancel"
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as ex:
        logging.error(ex)
    # Очищаем текущее состояние пользователя
    await state.clear()
    # Отправляем пустой ответ на callback query
    await call.answer()

# Импортируем необходимые модули
import logging
from aiogram import types, F
from aiogram.filters import Command, CommandObject
from keyboards import default
from utils import queries
from database import SessionLocal
from loader import dp, bot
import keyboards

# Определяем обработчик для команды "/start"
@dp.message(Command("start"))
async def cmd_start(message: types.Message, command: CommandObject):
    # Если команда "/start" содержит аргумент "777", отправляем сообщение "XD"
    if command.args and command.args == '777':
        await message.answer("XD")
        return
    # Иначе приветствуем пользователя и отправляем ему клавиатуру с основными командами
    await message.answer(f"{message.from_user.act_full_name}, привет 👋", reply_markup=keyboards.default.main_menu)

# Определяем обработчик для сообщений с медиафайлами (фото, видео, документы, видеозаметки)
@dp.message(F.content_type.in_({'photo', 'video', 'document', 'video_note'}))
async def echo_files(message: types.Message):
    # Если пользователь является администратором, отправляем ему file_id медиафайла
    if str(message.from_user.id) in keyboards.ADMINS:
        if message.photo:
            await message.answer(message.photo[0].file_id)
        elif message.video:
            await message.answer(message.video.file_id)
        elif message.document:
            await message.answer(message.document.file_id)
        elif message.video_note:
            await message.answer(message.video_note.file_id)
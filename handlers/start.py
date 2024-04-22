import logging

from aiogram import types, F
from aiogram.filters import Command, CommandObject

import keyboards
from data.config import ADMINS
from database import SessionLocal
from loader import dp, bot
from utils.db.queries import get_user, create_user


@dp.message(Command("start"))
# @dp.message(CommandStart(deep_link=True))
async def cmd_start(message: types.Message,
                    command: CommandObject):
    try:
        async with SessionLocal.begin() as session:
            user = await get_user(session,
                                  message.from_user.id)
            if user is None:
                await create_user(session,
                                  message.from_user.id,
                                  message.from_user.username,
                                  message.from_user.full_name)
            # session.commit()  # БОЛЬШЕ НЕ ИСПОЛЬЗУЕМ. АВТОКОММИТ РАБОТАЕТ
    except Exception as ex:
        logging.error(ex)
        try:
            await bot.send_message(message.from_user.id, '''Произошла ошибка. Начните с начала -> /start''')
        except Exception as ex:
            logging.error(ex)
        return
    if command.args:
        if command.args == '777':
            try:
                await bot.send_message(message.from_user.id, 'XD')
            except Exception as ex:
                logging.error(ex)
            return
    try:
        await bot.send_message(message.from_user.id, f'''{message.from_user.full_name}, привет 👋''',
                               reply_markup=keyboards.default.main_menu.main_menu)
    except Exception as ex:
        logging.error(ex)
        pass


@dp.message(F.content_type.in_({'photo', 'video', 'document', 'video_note'}))
async def echo_files(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        if message.photo:
            try:
                await bot.send_message(message.from_user.id, message.photo[0].file_id)
            except:
                pass
        if message.video:
            try:
                await bot.send_message(message.from_user.id, message.video.file_id)
            except:
                pass
        if message.document:
            try:
                await bot.send_message(message.from_user.id, message.document.file_id)
            except:
                pass
        if message.video_note:
            try:
                await bot.send_message(message.from_user.id, message.video_note.file_id)
            except:
                pass
        return


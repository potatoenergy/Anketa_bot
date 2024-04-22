from aiogram import F, types
from aiogram.types import Location, ReplyKeyboardRemove

from states.data_collection import Form
from aiogram.fsm.context import FSMContext
from loader import dp, bot
from aiogram.filters import StateFilter, Command
import keyboards


@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Введите адрес, либо нажмите на кнопку ниже для отправки геолокации",
        reply_markup=keyboards.default.main_menu.geo_button
    )
    await state.set_state(Form.location)

@dp.message(Form.location)
async def process_location(message: types.Message, state: FSMContext):
    if message.location is not None:
        await state.update_data(location=f'{message.location.latitude}, {message.location.longitude}')
    else:
        await state.update_data(location=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Отправьте фото",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Form.photo)
